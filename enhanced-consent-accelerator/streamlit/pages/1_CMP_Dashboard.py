import streamlit as st
import pandas as pd
from utils.connect import run_download_data
import plotly.express as px
import os

data_sources = st.session_state['data_sources']
_WAREHOUSE = st.session_state['_WAREHOUSE']

# Button to re-run and load the data
if st.button('Refresh Data'):
    run_download_data(_WAREHOUSE, data_sources)

# Load the data from local files
data = dict()
data_load_state = st.text("Loading data...")

data['cmp_load_times'] = pd.read_csv(os.path.join('data', 'cmp_load_times.csv'))
data['cmp_stats'] = pd.read_csv(os.path.join('data', 'cmp_stats.csv'))

data_load_state.text("")

st.header("CMP Dashboard")
st.subheader("View additional metrics related to CMP visible time")

c1, c2, c3 = st.columns((8, 1, 8))

with c1:
    data['cmp_stats'] = data['cmp_stats'].rename(columns = {'cmp load time' : 'CMP load time',
                                                            'first consent event type': 'First consent event type',
                                                            'cmp interaction time': 'CMP interaction time'
                                                            })
    fig = px.scatter(data['cmp_stats'], x='CMP load time', y='First consent event type', width=700, height=400, title="<b> CMP load time vs consent choice<b>")
    fig.update_layout(
        margin=dict(l=20, r=20, t=80, b=40),
    )
    st.plotly_chart(fig)

with c3:
    fig = px.scatter(data['cmp_stats'], x='CMP interaction time', y='First consent event type', width=700, height=400, title="<b> CMP interaction time vs consent choice<b>")
    fig.update_layout(
        margin=dict(l=20, r=20, t=80, b=40),
    )
    st.plotly_chart(fig)

custom_order =['within 2 sec', 'between 2 and 5 seconds', 'between 5 and 10 seconds', 'between 10 and 30 seconds', 'after 30+ seconds']
colours = ['green', 'lightgreen', 'orange', 'crimson']
fig = px.pie(data['cmp_load_times'], values=data['cmp_load_times']["value"], names=data['cmp_load_times']["base"],
color = data['cmp_load_times']["base"], color_discrete_map={
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
