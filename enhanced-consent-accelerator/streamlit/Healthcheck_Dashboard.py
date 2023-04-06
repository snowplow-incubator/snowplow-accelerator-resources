import streamlit as st
import plotly.express as px
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import os
from utils.connect import run_download_data


def main():

    _WAREHOUSE = 'snowflake'
    _supported_warehouse = ['snowflake', 'bigquery', 'databricks']

    data_sources = [
        ('consent_scopes', 'consent_scopes'),
        ('consent_types', 'consent_types'),
        ('consent_totals', 'consent_totals'),
        ('cmp_load_times', 'cmp_load_times'),
        ('cmp_stats', 'cmp_stats'),
        ('changelog', 'changelog'),
        ('users', 'users'),
        ('lookup', 'lookup')
    ]

    st.set_page_config(layout="wide", page_title="CONSENT DASHBOARD", page_icon=":bar_chart:", initial_sidebar_state="expanded")
    st.title("Consent Healthcheck Dashoard")

    if _WAREHOUSE.lower() not in _supported_warehouse:
        if _WAREHOUSE == 'CHANGE_ME':
            raise ValueError(f'Please change _WAREHOUSE variable in the `Dashboard.py` file on line 8 to your warehouse choice, one of {_supported_warehouse}')
        else:
            raise ValueError(f'{_WAREHOUSE} is not a currently supported warehouse, please choose from {_supported_warehouse}')


    if '_WAREHOUSE' not in st.session_state:
        st.session_state['_WAREHOUSE'] = _WAREHOUSE.lower()
    if 'data_sources' not in st.session_state:
        st.session_state['data_sources'] = data_sources

    data_sources = st.session_state['data_sources']
    _WAREHOUSE = st.session_state['_WAREHOUSE']

    # Button to re-run and load the data
    if st.button('Refresh Data'):
        run_download_data(_WAREHOUSE.lower(), data_sources)

    # Load the data from local files
    data = dict()
    data_load_state = st.text("Loading data...")
    data['consent_scopes'] = pd.read_csv(os.path.join('data', 'consent_scopes.csv'))
    data['consent_types'] = pd.read_csv(os.path.join('data', 'consent_types.csv'))
    data['consent_totals'] = pd.read_csv(os.path.join('data', 'consent_totals.csv'))

    data_load_state.text("")
    st.markdown('#')

    c1, c2, c3, c4, c5, c6, c7 = st.columns([1, 1, 1, 1, 1, 1, 1])

    with c1:
        st.metric(
            value="{0:,.0f}".format(data['consent_totals']["total_visitors"][0]),
            label="Total Visitors",
        )
    with c2:
        st.metric(
            value="{0:,.0f}".format(data['consent_totals']["allow"][0]),
            label="Consent Granted",
        )
    with c3:
        st.metric(
            value="{0:,.0f}".format(data['consent_totals']["withdrawn"][0]),
            label="Consent Withdrawn",
        )
    with c4:
        st.metric(
            value="{0:,.0f}".format(data['consent_totals']["pending"][0]),
            label="Consent Pending",
        )
    with c5:
        st.metric(
            value=str(data['consent_totals']["expired"][0]),
            label="Consent Expired",
        )
    with c6:
        st.metric(
            value="{0:,.0f}".format(data['consent_totals']["denied"][0]),
            label="Consent Denied",
        )
    with c7:
        st.metric(
            value="{0:,.0f}".format(data['consent_totals']["expires_in_six_months"][0]),
            label="Consent Expiring in <6 Months",
        )


    st.markdown("""---""")

    # Chart row
    c1, c2 = st.columns((2, 2))

    with c1:
        custom_order =['Consent Granted', 'Partially Granted (Customised)', 'Denied', 'Expired', 'Withdrawn', 'Consent Pending']
        fig = px.pie(data['consent_types'], values=data['consent_types']["value"], names=data['consent_types']["base"],
        color = data['consent_types']["base"],
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
        fig3 = px.bar(data['consent_scopes'], x=data['consent_scopes']["scope"], y=data['consent_scopes']["total_consent"], color = data['consent_scopes']["scope"],
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
