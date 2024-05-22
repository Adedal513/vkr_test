from cassandra.cluster import Cluster
import pandas as pd
import streamlit as st

@st.cache_resource
def get_cassadra_cluster():
    cluster = Cluster(['158.160.89.227'])
    session = cluster.connect('main')
    return session

@st.cache_data
def query_db(query: str):
    con = get_cassadra_cluster()
    result = con.execute(query)
    df = pd.DataFrame(list(result))
    return df

EXPLANATION_TEXT = """
### Правила модерации
Доступные для модерации классы:
- **normal** (отсутствие деструктивных смыслов)
- **insult** (оскорбления и унижающие достоинство формулировки)
- **threat** (угрозы физического и психического насилия)
- **obscenity** (угрозы сексуального характера и упоминание откровенных тем)

**Прошедшими модерацию** считаются сообщения, чья токсичность не превышает *30%*
"""