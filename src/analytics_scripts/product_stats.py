from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as F
from pyspark.sql.functions import *
from pyspark.sql.window import Window

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

df_classes = df.select(
    col('message_id'),
    col('product_category'),
    explode('classes').alias("class", "pred")
)

statsDF = df_classes.withColumn(
    "class_rating",
    row_number().over(
       Window.partitionBy("message_id") \
        .orderBy(desc("pred"))
    )
).filter(
    (col('class_rating') == 1) & (col('class') != 'non-toxic')
)

filteredDF = statsDF.groupBy(col('product_category'), col('class')).agg(count(F.lit(1)).alias('amount'))

filteredDF.write \
    .format("org.apache.spark.sql.cassandra") \
    .options(table="product_category_stats", keyspace="main") \
    .mode("overwrite") \
    .save()