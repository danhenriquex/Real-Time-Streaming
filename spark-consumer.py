import logging

from cassandra.cluster import Cluster
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StringType, StructField, StructType


def create_keyspace(session):
    session.execute(
        """
        CREATE KEYSPACE IF NOT EXISTS property_streams
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
    """
    )

    print("Keyspace created successfully!")


def create_table(session):
    session.execute(
        """
    CREATE TABLE IF NOT EXISTS property_streams.properties (
        price text,
        title text,
        link text,
        floor_plan text,
        address text,
        bedrooms text,
        bathrooms text,
        receptions text,
        epc_rating text,
        tenure text,
        time_remaning_on_lease text,
        service_charge text,
        council_tax_band text,
        ground_rent text,
        PRIMARY KEY (link)
        );
    """
    )

    print("Table created successfully!")


def insert_data(session, **kwargs):
    print("Inserting data...")

    print("Data before insert: ", kwargs.values())

    session.execute(
        """
    INSERT INTO property_streams.properties (
        price,
        title,
        link,
        floor_plan,
        address,
        bedrooms,
        bathrooms,
        receptions,
        epc_rating,
        tenure,
        time_remaning_on_lease,
        service_charge,
        council_tax_band,
        ground_rent
    )
    VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
    """,
        kwargs.values(),
    )

    print("Data inserted successfully!")


def create_cassandra_session():
    session = Cluster(["localhost"]).connect()

    print("Session: ", session)

    if session is not None:
        create_keyspace(session)
        create_table(session)

    return session


def main():
    logging.basicConfig(level=logging.INFO)

    spark = (
        SparkSession.builder.appName("RealEstateConsumer")
        .config("spark.cassandra.connection.host", "localhost")
        .config(
            "spark.jar.packages",
            "com.datastax.spark:spark-cassandra-connector_2.12:3.5.0,"
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0",
        )
        .getOrCreate()
    )

    kafka_df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "localhost:9092")
        .option("subscribe", "properties")
        .option("startingOffsets", "earliest")
        .load()
    )

    schema = StructType(
        [
            StructField("price", StringType(), True),
            StructField("title", StringType(), True),
            StructField("link", StringType(), True),
            StructField("floor_plan", StringType(), True),
            StructField("address", StringType(), True),
            StructField("bedrooms", StringType(), True),
            StructField("bathrooms", StringType(), True),
            StructField("receptions", StringType(), True),
            StructField("tenure", StringType(), True),
            StructField("time_remaining_on_lease", StringType(), True),
            StructField("service_charge", StringType(), True),
            StructField("EPC Rating", StringType(), True),
            StructField("council_tax_band", StringType(), True),
            StructField("ground_rent", StringType(), True),
        ]
    )

    kafka_df = (
        kafka_df.selectExpr("CAST(value as STRING) as value")
        .select(from_json(col("value"), schema).alias("data"))
        .select("data.*")
    )

    cassandra_query = (
        kafka_df.writeStream.foreachBatch(
            lambda batch_df, batch_id: batch_df.foreach(
                lambda row: insert_data(create_cassandra_session(), **row.asDict())
            )
        )
        .start()
        .awaitTermination()
    )


if __name__ == "__main__":
    main()
