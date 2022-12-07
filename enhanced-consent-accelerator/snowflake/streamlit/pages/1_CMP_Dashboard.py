import streamlit as st
import pandas as pd
from utils.connect import get_data, connect_to_snowflake, disconnect_from_snowflake
import plotly.express as px

# getting data from Snowflake
data_load_state = st.text("Loading data...")
cs, cnx = connect_to_snowflake()
df_cmp_load_times = get_data(cs, "queries/cmp_load_times.sql")
df_cmp_stats = get_data(cs, "queries/cmp_stats.sql")
disconnect_from_snowflake(cs, cnx)
data_load_state.text("")

st.header("CMP Dashboard")
st.subheader("View additional metrics related to CMP visible time")

c1, c2, c3 = st.columns((8, 1, 8))

with c1:
    fig = px.scatter(df_cmp_stats, x='CMP load time', y='First consent event type', width=700, height=400, title="<b> CMP load time vs consent choice<b>")
    fig.update_layout(
        margin=dict(l=20, r=20, t=80, b=40),
    )
    st.plotly_chart(fig)

with c3:
    fig = px.scatter(df_cmp_stats, x='CMP interaction time', y='First consent event type', width=700, height=400, title="<b> CMP interaction time vs consent choice<b>")
    fig.update_layout(
        margin=dict(l=20, r=20, t=80, b=40),
    )
    st.plotly_chart(fig)

custom_order =['within 2 sec', 'between 2 and 5 seconds', 'between 5 and 10 seconds', 'between 10 and 30 seconds', 'after 30+ seconds']
colours = ['green', 'lightgreen', 'orange', 'crimson']
fig = px.pie(df_cmp_load_times, values=df_cmp_load_times["VALUE"], names=df_cmp_load_times["BASE"],
color = df_cmp_load_times["BASE"], color_discrete_map={
                                                        'within 2 sec': 'green',
                                                        'between 2 and 5 seconds': 'lightgreen',
                                                        'between 5 and 10 seconds': 'gold',
                                                        'between 10 and 30 seconds': 'orange',
                                                        'after 30+ seconds': 'crimson'
                                                    }, hole=0.4,  category_orders = {'BASE': custom_order})
fig.update_layout(
title="<b>Elapsed time till CMP appears for visitors</b>")
fig.update_traces(textposition='inside')
st.plotly_chart(fig)
