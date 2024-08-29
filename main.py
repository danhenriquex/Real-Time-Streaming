import asyncio
import json
import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from kafka import KafkaProducer
from openai import OpenAI
from playwright.async_api import async_playwright

from constants import properties, properties_2

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("OPENAI_API_KEY")
SBR_WS_CDP = os.getenv("SBR_WS_CDP")
BASE_URL = os.getenv("BASE_URL")
LOCATION = os.getenv("LOCATION")

client = OpenAI(api_key=api_key)


def extract_picture(picture_section):
    picture_sources = []

    for picture in picture_section.find_all("picture"):
        for source in picture.find_all("source"):
            source_type = source.get("type", "").split("/")[-1]
            pic_url = source.get("srcset", "").split(",")[0].split(" ")[0]

            if source_type == "webp" and "1024" in pic_url:
                picture_sources.append(pic_url)

    return picture_sources


def extract_property_details(input_value):
    print("Extracting property details...")

    command = f"""
        You are a data extractor model and you have been tasked with extracting information about the apartment for me into json.
        Here is the div for the property details:

        {input_value}

        this is the final json structure expected:
        {{
          "price": "",
          "address": "",
          "bedrooms": "",
          "bathrooms": "",
          "reception": "",
          "EPC_Rating": "",
          "tenure": "",
          "time_remaining_on_lease": "",
          "service_charge": "",
          "council_tax_band": "",
          "ground_rent": "",
        }}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": command},
        ],
    )

    res = response.choices[0].message.content
    json_data = json.loads(res)

    return json_data


def extract_floor_plan(soup):
    print("Extracting floor plan")

    plan = {}
    floor_plan = soup.find("div", {"data-testid": "floorplan-thumbnail-0"})

    if floor_plan:
        floor_plan_src = floor_plan.find("picture").find("source")["srcset"]
        plan["floor_plan"] = floor_plan_src.split(" ")[0]

    return plan


async def bright_data_extraction(pw, producer):
    browser = await pw.chromium.connect_over_cdp(SBR_WS_CDP)
    try:
        page = await browser.new_page()
        print(f"Connected! Navigating to ${BASE_URL}")
        await page.goto(BASE_URL)

        # enter london in the search bar and press enter to search

        await page.fill('input[name="autosuggest-input"]', LOCATION)
        await page.keyboard.press("Enter")

        print("Waiting for search results...")

        content = await page.inner_html('div[data-testid="regular-listings"]')

        soup = BeautifulSoup(content, features="html.parser")

        for idx, div in enumerate(soup.find_all("div", class_="dkr2t83")):
            data = {}
            address = div.find("address").text
            title = div.find("h2").text
            link = div.find("a")["href"]

            data.update({"address": address, "title": title, "link": BASE_URL + link})

            # goto the listing page
            print("Navigating to the listing page", link)

            await page.goto(data["link"])
            await page.wait_for_load_state("load")

            content = await page.inner_html('div[class="_1olqsf95 _1olqsf94"]')
            soup = BeautifulSoup(content, features="html.parser")

            picture_section = soup.find("ol", {"aria-label": "Gallery images"})

            pictures = extract_picture(picture_section)

            data["pictures"] = pictures

            property_details = soup.select_one('div[class="_14bi3x331"]')
            property_details = extract_property_details(property_details)

            floor_plan = extract_floor_plan(soup)

            data.update(floor_plan)
            data.update(property_details)

            # print("data: ", data)

            print("Sending data to Kafka")
            producer.send("properties", value=json.dumps(data).encode("utf-8"))
            print("Data sent to Kafka")

    finally:
        await browser.close()


def run(producer):
    print("Connecting to Scraping Browser...")

    # For mocked data you can use the code below

    for idx, item in enumerate(properties_2):
        print(f"Processing property {idx + 1} of {len(properties)}")
        print("Sending data to Kafka")
        producer.send("properties", value=json.dumps(item).encode("utf-8"))
        print("Data sent to Kafka")

    # If you want to use a webscrapper from brightdata you can use the function below
    # Be aware that sometimes the div's id change, so you have to update it
    # await bright_data_extraction(pw, producer)


def main():
    producer = KafkaProducer(bootstrap_servers=["localhost:9092"], max_block_ms=5000)
    run(producer)


if __name__ == "__main__":
    main()
