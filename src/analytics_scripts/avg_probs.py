from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as F
from pyspark.sql.functions import *

spark = SparkSession \
    .builder \
    .appName("Streaming from Kafka") \
    .config("spark.streaming.stopGracefullyOnShutdown", True) \
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0') \
    .config("spark.cassandra.connection.host", "158.160.89.227") \
    .config("spark.sql.extensions", "com.datastax.spark.connector.CassandraSparkExtensions") \
    .config("spark.sql.shuffle.partitions", 4) \
    .config('confirm.truncate', True) \
    .master("local[*]") \
    .getOrCreate()

df = spark.read\
        .format("org.apache.spark.sql.cassandra")\
        .options(table='messages', keyspace='main')\
        .load()

avg_preds = df.select(
    explode(col('classes')).alias("class", "pred")
).groupBy("class").agg(
    avg("pred").alias("avg_prob")
)

avg_preds.write.format("org.apache.spark.sql.cassandra") \
    .options(table="avg_probs", keyspace="main").mode("overwrite").save()