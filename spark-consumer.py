import logging

from cassandra.cluster import Cluster
from pyspark.sql import SparkSession


def main():
    logging.basicConfig(level=logging.INFO)

    spark = (
        SparkSession.builder.appName("SparkConsumer")
        .config("spark.cassandra.connection.host", "localhost")
        .config("spark.jar.packages", "com.datastax.spark")
    )


if __name__ == "__main__":
    main()
