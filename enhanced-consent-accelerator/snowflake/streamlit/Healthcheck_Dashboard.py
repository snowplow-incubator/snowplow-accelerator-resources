from utils.connect import get_data, connect_to_snowflake, disconnect_from_snowflake
import streamlit as st
import plotly.express as px
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

def main():
    st.set_page_config(layout="wide", page_title="CONSENT DASHBOARD", page_icon=":bar_chart:", initial_sidebar_state="expanded")
    st.title("Consent Healthcheck Dashoard")

    # getting data from Snowflake
    data_load_state = st.text("Loading data...")
    cs, cnx = connect_to_snowflake()
    df_consent_scopes = get_data(cs, "queries/consent_scopes.sql")
    df_consent_types = get_data(cs, "queries/consent_types.sql")
    df_consent_totals = get_data(cs, "queries/consent_totals.sql")
    disconnect_from_snowflake(cs, cnx)

    data_load_state.text("")
    st.markdown('#')

    c1, c2, c3, c4, c5, c6, c7 = st.columns([1, 1, 1, 1, 1, 1, 1])

    with c1:
        st.metric(
            value="{0:,.0f}".format(df_consent_totals["TOTAL_VISITORS"][0]),
            label="Total Visitors",
        )
    with c2:
        st.metric(
            value="{0:,.0f}".format(df_consent_totals["ALLOW"][0]),
            label="Consent Granted",
        )
    with c3:
        st.metric(
            value="{0:,.0f}".format(df_consent_totals["WITHDRAWN"][0]),
            label="Consent Withdrawn",
        )
    with c4:
        st.metric(
            value="{0:,.0f}".format(df_consent_totals["PENDING"][0]),
            label="Consent Pending",
        )
    with c5:
        st.metric(
            value=str(df_consent_totals["EXPIRED"][0]),
            label="Consent Expired",
        )
    with c6:
        st.metric(
            value="{0:,.0f}".format(df_consent_totals["DENIED"][0]),
            label="Consent Denied",
        )
    with c7:
        st.metric(
            value="{0:,.0f}".format(df_consent_totals["EXPIRES_IN_SIX_MONTHS"][0]),
            label="Consent Expiring in <6 Months",
        )


    st.markdown("""---""")

    # Chart row
    c1, c2, c3 = st.columns((2, 1, 2))

    with c1:
        custom_order =['Consent Granted', 'Partially Granted (Customised)', 'Denied', 'Expired', 'Withdrawn', 'Consent Pending']
        fig = px.pie(df_consent_types, values=df_consent_types["VALUE"], names=df_consent_types["BASE"],
        color = df_consent_types["BASE"],
        color_discrete_map={
            'Consent Granted': 'green',
            'Partially Granted (Customised)': 'lightgreen',
            'Denied': 'orange',
            'Expired': 'crimson',
            'Withdrawn': 'gold',
            'Consent Pending': 'grey'
        }, hole=0.4,  category_orders = {'BASE': custom_order})
        fig.update_layout(
        title="<b>Proportion of users by latest consent status</b>")
        fig.update_traces(textposition='inside')
        st.plotly_chart(fig)

    with c2:
        colours = []
        fig3 = px.bar(df_consent_scopes, x=df_consent_scopes["SCOPE"], y=df_consent_scopes["TOTAL_CONSENT"], color = df_consent_scopes["SCOPE"],
         color_discrete_map={
        'marketing': 'DarkBlue',
        'statistics': 'RoyalBlue',
        'necessary': 'LightSkyBlue',
        'preferences': 'LightSteelBlue'
    })
        fig3.update_layout(
        title="<b>Consent by Scope</b>")
        st.plotly_chart(fig3)

    st.markdown("""---""")

if __name__ == "__main__":
    main()
