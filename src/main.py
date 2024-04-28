from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as F
from pyspark.sql.functions import *
from utils import udf_api_call, cassandra_sink

spark = SparkSession \
    .builder \
    .appName("Streaming from Kafka") \
    .config("spark.streaming.stopGracefullyOnShutdown", True) \
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0') \
    .config("spark.cassandra.connection.host", "84.201.162.146") \
    .config("spark.sql.extensions", "com.datastax.spark.connector.CassandraSparkExtensions") \
    .config("spark.sql.shuffle.partitions", 4) \
    .master("local[*]") \
    .getOrCreate()

schema = StructType(
    [
        StructField("text", StringType(), True), # Непосредственный текст сообщения
        StructField("user_id", StringType(), True), # ID пользователя
        StructField("created_at", StringType(), True), # Дата создания сообщения
        StructField("product_category", StringType(), True) # Категория продукта
    ]
)

df = spark\
      .readStream \
      .format("kafka") \
      .option("kafka.bootstrap.servers", "51.250.23.86:9092") \
      .option("subscribe", "text-messages") \
      .option("startingOffsets", "earliest") \
      .load()

raw_data = df.selectExpr(
    "CAST(key AS STRING)",
    "CAST(value AS STRING)"
).withColumn(
    "deserialized_data",
    F.from_json(
        col("value"),
        schema
    )
).select(
    col("key").alias("message_id"),
    col("deserialized_data.*")
)

query = raw_data.withColumn(
    "classes",
    udf_api_call(col("text"))
)

res = query.writeStream.foreachBatch(cassandra_sink).start()

res.awaitTermination()