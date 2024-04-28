import requests
import json
from pyspark.sql.functions import udf, col, explode
from pyspark.sql.types import StructType, StructField, DoubleType, StringType, MapType
from pyspark.sql import Row
from http import HTTPStatus


def cassandra_sink(df, epoch_id):
    df.write.format("org.apache.spark.sql.cassandra")\
        .options(table="messages", keyspace="main").mode("append").save()

def execute_api_call(message_text: str) -> dict:
    """
    Обращается к API Torchserve и возвращает вероятности с классами.
    
    """
    headers = {
        'Content-Type': "application/json"
    }

    res = None
    request_body = {
        "text": message_text
    }

    res = requests.post(
        "http://localhost:8080/predictions/toxicity",
        json=request_body,
        headers=headers
    )
    
    res.raise_for_status()

    if res != None and res.status_code == HTTPStatus.OK:
        return json.loads(res.text)
    
response_schema = MapType(StringType(), StringType())
udf_api_call = udf(execute_api_call, response_schema)