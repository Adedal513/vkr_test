import requests
import json
from pyspark.sql.functions import udf, col, explode
from pyspark.sql.types import StructType, StructField, DoubleType
from pyspark.sql import Row
from http import HTTPStatus

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
    
response_schema = StructType([
    StructField("non-toxic", DoubleType()),
    StructField("insult", DoubleType()),
    StructField("threat", DoubleType()),
    StructField("obscinity", DoubleType()),
])

udf_api_call = udf(execute_api_call, response_schema)