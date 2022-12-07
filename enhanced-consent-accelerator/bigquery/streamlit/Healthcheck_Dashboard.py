from google.oauth2 import service_account
import streamlit as st
import plotly.express as px
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
st.secrets["gcp_service_account"]
)

# Please modify this variable to be in line with your derived schema
schema = "{your_derived_schema}"

def main():
    st.set_page_config(layout="wide", page_title="CONSENT DASHBOARD", page_icon=":bar_chart:", initial_sidebar_state="expanded")
    st.title("Consent Healthcheck Dashboard")

    # getting data from BigQuery
    data_load_state = st.text("Loading data...")

    consent_scopes_query = "select scope, total_consent from " + schema + ".snowplow_web_consent_scope_status"
    df_consent_scopes = pd.read_gbq(consent_scopes_query,credentials=credentials)

    consent_types_query = """select
                                'Consent Granted' as base,
                                count(case when is_latest_version is True and last_consent_event_type='allow_all' then 1 end) as value
                            from """ + schema + """.snowplow_web_consent_users

                            union all

                            select
                                'Partially Granted (Customised)' as base,
                                count(case when is_latest_version is True and last_consent_event_type ='allow_selected' then 1 end) as value
                            from """ + schema + """.snowplow_web_consent_users

                            union all

                            select
                                'Consent Pending' as base,
                                count(case when is_latest_version is True and last_consent_event_type = 'pending' then 1 end) as value
                            from """ + schema + """.snowplow_web_consent_users

                            union all

                            select
                                'Denied' as base,
                                count(case when is_latest_version is True and last_consent_event_type = 'deny_all'  then 1 end) as value
                            from """ + schema + """.snowplow_web_consent_users

                            union all

                            select
                                'Expired' as base,
                                count(case when is_latest_version is True and last_consent_event_type = 'expired'  then 1 end) as value
                            from """ + schema + """.snowplow_web_consent_users

                            union all

                            select
                                'Withdrawn' as base,
                                count(case when is_latest_version is True and last_consent_event_type = 'withdrawn'  then 1 end) as value
                            from """ + schema + """.snowplow_web_consent_users
                            """
    df_consent_types = pd.read_gbq(consent_types_query,credentials=credentials)

    consent_totals_query = "select * from  " + schema + ".snowplow_web_consent_totals"
    df_consent_totals = pd.read_gbq(consent_totals_query,credentials=credentials)

    data_load_state.text("")
    st.markdown('#')

    c1, c2, c3, c4, c5, c6, c7 = st.columns([1, 1, 1, 1, 1, 1, 1])

    with c1:
        st.metric(
            value="{0:,.0f}".format(df_consent_totals["total_visitors"][0]),
            label="Total Visitors",
        )
    with c2:
        st.metric(
            value="{0:,.0f}".format(df_consent_totals["allow"][0]),
            label="Consent Granted",
        )
    with c3:
        st.metric(
            value="{0:,.0f}".format(df_consent_totals["withdrawn"][0]),
            label="Consent Withdrawn",
        )
    with c4:
        st.metric(
            value="{0:,.0f}".format(df_consent_totals["pending"][0]),
            label="Consent Pending",
        )
    with c5:
        st.metric(
            value=str(df_consent_totals["expired"][0]),
            label="Consent Expired",
        )
    with c6:
        st.metric(
            value="{0:,.0f}".format(df_consent_totals["denied"][0]),
            label="Consent Denied",
        )
    with c7:
        st.metric(
            value="{0:,.0f}".format(df_consent_totals["expires_in_six_months"][0]),
            label="Consent Expiring in <6 Months",
        )


    st.markdown("""---""")

    # Chart row
    c1, c2, c3 = st.columns((2, 1, 2))

    with c1:
        custom_order =['Consent Granted', 'Partially Granted (Customised)', 'Denied', 'Expired', 'Withdrawn', 'Consent Pending']
        fig = px.pie(df_consent_types, values=df_consent_types["value"], names=df_consent_types["base"],
        color = df_consent_types["base"],
        color_discrete_map={
            'Consent Granted': 'green',
            'Partially Granted (Customised)': 'lightgreen',
            'Denied': 'orange',
            'Expired': 'crimson',
            'Withdrawn': 'gold',
            'Consent Pending': 'grey'
        }, hole=0.4,  category_orders = {'base': custom_order})
        fig.update_layout(
        title="<b>Proportion of Users by Latest Consent Status</b>")
        fig.update_traces(textposition='inside')
        st.plotly_chart(fig)

    with c2:
        fig3 = px.bar(df_consent_scopes, x=df_consent_scopes["scope"], y=df_consent_scopes["total_consent"], color = df_consent_scopes["scope"],
         color_discrete_map={
        'marketing': 'DarkBlue',
        'statistics': 'RoyalBlue',
        'necessary': 'LightSkyBlue',
        'preferences': 'LightSteelBlue'
    }, labels={'scope': "Consent Scope", "total_consent": "Total Users"})
        fig3.update_layout(
        title="<b>Consent by Scope</b>")
        st.plotly_chart(fig3)

    st.markdown("""---""")

if __name__ == "__main__":
    main()
