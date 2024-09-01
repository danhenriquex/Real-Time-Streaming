<h1 align="center">🚗 Data Project</h1>
<p align="center" id="objetivo">Learning Data Engineering.</p>

<a href="https://wakatime.com/badge/user/8028aaab-232d-4832-8b66-f103e1d713b9/project/6ac45fa8-dfae-463f-bca1-a84418e4883c"><img src="https://wakatime.com/badge/user/8028aaab-232d-4832-8b66-f103e1d713b9/project/6ac45fa8-dfae-463f-bca1-a84418e4883c.svg" alt="wakatime"></a>

<p align="center">
 <a href="#overview">Overview</a> •
 <a href="#features">Technologies and Tools Used</a> •
 <a href="#roadmap">Project Structure</a> • 
 <a href="#tecnologias">Getting Started</a> • 
 <a href="#author">Running the Pipeline</a>
<a href="#author">What I Learned</a>
</p>

<h4 align="center"> 
	🚧  Data Engineering Project 🚀 Finished  🚧
</h4>

### Overview

<div style='margin: 20px' id="overview">
This project demonstrates a data processing pipeline using Kafka, PySpark, Docker, Cassandra, and OpenAI. The goal was to create a system for real-time data streaming and processing, integrating various technologies to build a scalable and efficient architecture.
</div>

### Features

<div id="features">

- **Kafka**: A distributed streaming platform used for building real-time data pipelines and streaming applications.
- **PySpark**: The Python API for Apache Spark, used for large-scale data processing and analytics.
- **Docker**: A platform for automating containerized applications, ensuring consistent environments across development, testing, and production.
- **Cassandra**: A distributed NoSQL database designed for handling large amounts of data across many commodity servers.
- **OpenAI**: Used for integrating advanced language models into the pipeline.
- **Python**: The primary programming language used for scripting and application logic.

</div>

<div id="roadmap">

### Project Structure


├── jobs/requirements.txt         

├── jobs/spark-consumer.py                

├── .env.example         

├── constants.py              

├── docker-compose.yml                 

├── main.py          
</div>


### Scripts Overview

- `jobs/requirements.txt`: Lists the Python dependencies required for the Spark consumer job.
- `jobs/spark-consumer.py`: Contains the code for consuming data from Kafka and processing it using PySpark.
- `.env.example`: An example environment variable file to configure your local environment.
- `constants.py`: Defines constants used throughout the project.
- `docker-compose.yml`: Defines and runs multi-container Docker applications, configuring services for Kafka, Cassandra, and other components.
- `main.py`: The main script to initialize and run the application.

<div id="tecnologias">
	
### Getting Started

To get started with this project, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
2. **Setup Environment**
   ```bash
   cp .env.example.env
3. **Run Docker Containers**
   ```bash
   docker compose up -d
4. **Execute the main script**
   ```bash
   python main.py

</div>

### What I learned

	
- Kafka Integration: Gained experience in using Kafka for real-time data streaming and message brokering.
- PySpark: Developed skills in large-scale data processing and analytics using PySpark.
- Docker: Learned to containerize applications and manage multi-container setups with Docker Compose.
- Cassandra: Worked with Cassandra for scalable and distributed database solutions.
- OpenAI API: Integrated OpenAI’s language models for advanced text processing and analysis.

</div>


### Author

---

<!-- <script type="text/javascript" src="https://platform.linkedin.com/badges/js/profile.js" async defer></script> -->

<div align="left" id="author">

<a href="https://github.com/danhenriquex">
  <img src="https://github.com/danhenriquex.png" width="100" height="100" style="border-radius: 50%"/>
</a>

<!-- <div class="LI-profile-badge"  data-version="v1" data-size="medium" data-locale="pt_BR" data-type="vertical" data-theme="dark" data-vanity="danilo-henrique-santana"><a class="LI-simple-link" href='https://br.linkedin.com/in/danilo-henrique-santana?trk=profile-badge'>Danilo Henrique</a></div> -->
</div>

<div style="margin-top: 20px" >
  <a href="https://www.linkedin.com/in/danilo-henrique-480032167/">
    <img  src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/>
  </a>
</div>

