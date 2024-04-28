from cassandra.cluster import Cluster
import pandas as pd
import streamlit as st

@st.cache_resource
def get_cassadra_cluster():
    cluster = Cluster(['158.160.70.90'])
    session = cluster.connect('main')
    return session

@st.cache_data
def query_db(query: str):
    con = get_cassadra_cluster()
    result = con.execute(query)
    df = pd.DataFrame(list(result))
    return df