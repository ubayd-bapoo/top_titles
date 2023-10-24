import sys
import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg
from pyspark.sql.window import Window


# Configure the logging settings
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
# Create a logger
logger = logging.getLogger(__name__)


class Spark:
    def __init__(self):
        logger.info("Reading Hadoop Data")
        spark = SparkSession.builder.appName("ReadTSV").getOrCreate()
        self._data_title_basic = spark.read\
            .option("delimiter", "\t")\
            .option("header", "true")\
            .option("inferSchema", "true")\
            .csv("hdfs://namenode:9000/user/root/daemon/title_basic.tsv")
        self._data_titles_ratings = spark.read\
            .option("delimiter", "\t")\
            .option("header", "true")\
            .option("inferSchema", "true")\
            .csv("hdfs://namenode:9000/user/root/daemon/titles_ratings.tsv")
        self.top_titles = {}
        self._start_up()

    def _start_up(self):
        logger.info("Total Rating: %s", str(self._data_titles_ratings.count()))
        logger.info("Total Titles: %s", str(self._data_title_basic.count()))
        filtered_df = self._data_titles_ratings.filter(col("numVotes") >= 100)

        # Calculate the ranking based on the provided formula
        ranking_expr = (col("numVotes") / avg(col("numVotes")).over(Window.partitionBy())) * col("averageRating")
        filtered_df = filtered_df.withColumn("ranking", ranking_expr)

        # Sort the DataFrame by ranking in descending order
        sorted_df = filtered_df.sort(col("ranking").desc())

        # Join the two DataFrames based on the "tconst" column
        top_titles_df = self._data_title_basic.filter(col("titleType") == "movie")
        top_titles_df = top_titles_df.join(sorted_df, on="tconst", how="inner")
        top_titles_df = top_titles_df.sort(col("ranking").desc()).limit(15)
        top_titles_df.show()

        self.top_titles = top_titles_df.toJSON().collect()

    def get_top_titles(self):
        return self.top_titles
