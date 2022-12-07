import streamlit as st
import pandas as pd
from Healthcheck_Dashboard import credentials, schema
import plotly.express as px

data_load_state = st.text("Loading data...")

cmp_stats_query = """select event_id,
                                domain_userid,
                                round(cmp_load_time, 2) as CMP_load_time,
                                cmp_tstamp,
                                first_consent_event_tstamp,
                                first_consent_event_type as first_consent_event_type,
                                cmp_interaction_time as CMP_interaction_time
                            from """ + schema + """.snowplow_web_consent_cmp_stats"""
df_cmp_stats= pd.read_gbq(cmp_stats_query,credentials=credentials)

cmp_load_times_query = """select
                            'within 2 sec' as base,
                            count(case when cmp_load_time <= 2 then 1 end) as value
                            from """ + schema + """.snowplow_web_consent_cmp_stats

                            union all

                            select
                            'between 2 and 5 seconds' as base,
                            count(case when cmp_load_time > 2 and cmp_load_time <= 5 then 1 end) as value
                            from """ + schema + """.snowplow_web_consent_cmp_stats

                            union all

                            select
                            'between 5 and 10 seconds' as base,
                            count(case when cmp_load_time >5 and cmp_load_time <= 10 then 1 end) as value
                            from """ + schema + """.snowplow_web_consent_cmp_stats

                            union all

                            select
                            'between 10 and 30 seconds' as base,
                            count(case when cmp_load_time >10 and cmp_load_time <= 30 then 1 end) as value
                            from """ + schema + """.snowplow_web_consent_cmp_stats

                            union all

                            select
                            'after 30+ seconds' as base,
                            count(case when cmp_load_time > 30 then 1 end) as value
                            from """ + schema + """.snowplow_web_consent_cmp_stats
                            """
df_cmp_load_times = pd.read_gbq(cmp_load_times_query,credentials=credentials)

data_load_state.text("")

st.header("CMP Dashboard")
st.subheader("View additional metrics related to CMP visible time")

c1, c2, c3 = st.columns((2, 2, 1))

with c1:
    fig = px.scatter(df_cmp_stats, x='CMP_load_time', y='first_consent_event_type', width=700, height=400, title="<b> CMP load time vs consent choice<b>")
    fig.update_layout(
        margin=dict(l=20, r=20, t=80, b=40),
    )
    st.plotly_chart(fig)

with c2:
    fig = px.scatter(df_cmp_stats, x='CMP_interaction_time', y='first_consent_event_type', width=700, height=400, title="<b> CMP interaction time vs consent choice<b>")
    fig.update_layout(
        margin=dict(l=20, r=20, t=80, b=40),
    )
    st.plotly_chart(fig)

custom_order =['within 2 sec', 'between 2 and 5 seconds', 'between 5 and 10 seconds', 'between 10 and 30 seconds', 'after 30+ seconds']
colours = ['green', 'lightgreen', 'orange', 'crimson']
fig = px.pie(df_cmp_load_times, values=df_cmp_load_times["value"], names=df_cmp_load_times["base"],
color = df_cmp_load_times["base"], color_discrete_map={
                                                        'within 2 sec': 'green',
                                                        'between 2 and 5 seconds': 'lightgreen',
                                                        'between 5 and 10 seconds': 'gold',
                                                        'between 10 and 30 seconds': 'orange',
                                                        'after 30+ seconds': 'crimson'
                                                    }, hole=0.4,  category_orders = {'base': custom_order})
fig.update_layout(
title="<b>Elapsed time till CMP appears for visitors</b>")
fig.update_traces(textposition='inside')
st.plotly_chart(fig)
