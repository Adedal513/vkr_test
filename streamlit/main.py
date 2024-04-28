import streamlit as st 
import matplotlib.pyplot as plt
import plotly.express as px
from plots import *
import plotly.graph_objects as go

def main():
    st.set_page_config(
        page_title="Модерация",
        page_icon="📈",
        layout="wide",
    )
    st.title("Модерация контента")

    kpi1, kpi2, kpi3 = st.columns(3)
    m1, m2, m3 = get_main_metrics()

    kpi1.metric(
        label="Всего",
        value=m1
    )
    kpi2.metric(
        label='Прошло модерацию ✅',
        value=m2
    )
    kpi3.metric(
        label='Не прошло модерацию ❌',
        value=m3
    )

    fig_col1, fig_col2 = st.columns(2)
    df = get_ts_df()

    with fig_col1:
        st.markdown("### Категоризаций")
        df = get_ts_df()
        fig = go.Figure([go.Scatter(x=df['created_at'], y=df['cnt'])])
        st.write(fig)
    with fig_col2:
        st.markdown('### Классы')
        fig = px.pie(df, values='cnt', names='category')
        st.write(fig)


if __name__ == '__main__':
    main()