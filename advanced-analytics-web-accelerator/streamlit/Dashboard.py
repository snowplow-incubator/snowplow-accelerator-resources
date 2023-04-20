import os
from utils.connect import run_download_data
import streamlit as st
import plotly.graph_objects as go
from utils.countries import data_by_country
import pandas as pd


def main():

    # Set headers and titles
    _WAREHOUSE = 'CHANGE_ME'
    _supported_warehouse = ['snowflake', 'databricks', 'bigquery']

    data_sources = [
        ('sessions/num_sessions_by_day', 'num_sessions_by_day'),
        ('sessions/num_sessions', 'num_sessions'),
        ('sessions/avg_duration_by_day', 'avg_duration_by_day'),
        ('sessions/avg_duration', 'avg_duration'),
        ('sessions/sessions_by_geo', 'sessions_by_geo'),
        ('sessions/sessions_by_device', 'sessions_by_device'),
        ('users/number_of_users', 'number_of_users'),
        ('pageviews/pageviews_by_day', 'pageviews_by_day'),
        ('pageviews/pageviews_by_page', 'pageviews_by_page'),
        ('pageviews/pageviews_by_referer', 'pageviews_by_referer'),
        ('sessions/bounce_rate_by_day', 'bounce_rate_by_day')
    ]

    if _WAREHOUSE.lower() not in _supported_warehouse:
        if _WAREHOUSE == 'CHANGE_ME':
            raise ValueError(f'Please change _WAREHOUSE variable in the `Dashboard.py` file on line 10 to your warehouse choice, one of {_supported_warehouse}')
        else:
            raise ValueError(f'{_WAREHOUSE} is not a currently supported warehouse, please choose from {_supported_warehouse}')


    if '_WAREHOUSE' not in st.session_state:
        st.session_state['_WAREHOUSE'] = _WAREHOUSE.lower()
    if 'data_sources' not in st.session_state:
        st.session_state['data_sources'] = data_sources

    data_sources = st.session_state['data_sources']
    _WAREHOUSE = st.session_state['_WAREHOUSE']

    st.set_page_config(layout="wide", page_title="Sessions")

    st.title("Snowplow Web Insights")

    # Button to re-run and load the data
    if st.button('Refresh Data'):
        run_download_data(_WAREHOUSE, data_sources)

    # Load the data from local files
    data = dict()
    data_load_state = st.text("Loading data...")
    for _, name in data_sources:
        data[name] = pd.read_csv(os.path.join('data', f'{name}.csv'))
    data_load_state.text("")

    st.subheader("Summary")

    col1, col2, col3 = st.columns([1, 3, 2])

    with col1:
        st.metric(
            value="{0:,.0f}".format(data['num_sessions']["number_of_sessions"][0]),
            label="Total Sessions",
        )
        st.metric(
            value=str(data['avg_duration']["average_session_engaged_time_in_s"][0]) + "s",
            label="Average Session Len",
        )
        st.metric(
            value="{0:,.0f}".format(data['number_of_users']["number_of_users"][0]),
            label="Total Users",
        )

    with col2:
        sessions_iso3 = data_by_country(data['sessions_by_geo'])

        fig = go.Figure(
            data=go.Choropleth(
                locations=sessions_iso3["iso_3"],
                z=sessions_iso3["number_of_sessions"],
                colorscale="Blues",
                showscale=False,
            )
        )

        fig.update_geos(
            visible=False,
            resolution=50,
            showcountries=True,
            countrycolor="LightGrey",
        )
        fig.update_layout(showlegend=False, dragmode=False)

        fig.update_layout(
            height=300,
            width=700,
            margin={"l": 20, "r": 20, "t": 25, "b": 0},
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
        )

        fig.update_layout(title_text="Sessions by Country")

        st.plotly_chart(fig, use_container_width=True)

    with col3:
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=data['sessions_by_device']["device_family"],
                    values=data['sessions_by_device']["number_of_sessions"],
                    hole=0.3,
                )
            ]
        )
        fig.update_layout(
            height=300,
            width=700,
            margin={"l": 20, "r": 20, "t": 25, "b": 0},
        )
        fig.update_layout(title_text="Sessions by Device    ")
        fig.update_traces(textposition="inside")
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode="hide")

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Sessions")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        fig = go.Figure(
            [
                go.Scatter(
                    x=data['num_sessions_by_day']["date"],
                    y=data['num_sessions_by_day']["number_of_sessions"],
                    fill="tozeroy",
                )
            ]
        )
        fig.update_layout(
            height=300,
            width=700,
            margin={"l": 20, "r": 20, "t": 25, "b": 0},
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
        )
        fig.update_layout(title_text="Total Sessions")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure(
            [
                go.Bar(
                    x=data['avg_duration_by_day']["date"],
                    y=data['avg_duration_by_day']["avg_engaged_time"],
                ),
            ]
        )
        fig.update_layout(
            title_text="Test",
            height=300,
            width=700,
            margin={"l": 20, "r": 20, "t": 25, "b": 0},
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
        )
        fig.update_layout(title_text="Average Session Duration")

        st.plotly_chart(fig, use_container_width=True)

    with col3:

        fig = go.Figure(
            [
                go.Scatter(
                    x=data['bounce_rate_by_day']["date"],
                    y=data['bounce_rate_by_day']["bouncerate"],
                    fill="tozeroy",
                )
            ]
        )

        fig.update_layout(
            height=300,
            width=700,
            margin={"l": 20, "r": 20, "t": 25, "b": 0},
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
        )
        fig.update_layout(title_text="Bounce Rate")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Pageviews")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        fig = go.Figure(
            [
                go.Bar(
                    x=data['pageviews_by_day']["date"],
                    y=data['pageviews_by_day']["number_of_pageviews"],
                ),
            ]
        )
        fig.update_layout(
            title_text="Test",
            height=300,
            width=700,
            margin={"l": 20, "r": 20, "t": 25, "b": 0},
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
        )
        fig.update_layout(title_text="Pageviews by Day")

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # st.table(pageviews_by_page)
        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=["", ""], line_color="white", fill_color="white"
                    ),
                    cells=dict(
                        values=[
                            data['pageviews_by_page']["page_title"],
                            data['pageviews_by_page']["number_of_pageviews"],
                        ],
                        align="left",
                        line_color=["white"],
                        fill_color=["white"],
                    ),
                )
            ]
        )
        fig.update_layout(
            height=300,
            width=700,
            margin={"l": 20, "r": 20, "t": 25, "b": 0},
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
        )
        fig.update_layout(title_text="Most Viewed Pages")

        st.plotly_chart(fig, use_container_width=False)
    with col3:
        # st.table(pageviews_by_page)
        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=["", ""], line_color="white", fill_color="white"
                    ),
                    cells=dict(
                        values=[
                            data['pageviews_by_referer']["refr_urlhost"],
                            data['pageviews_by_referer']["number_of_pageviews"],
                        ],
                        align="left",
                        line_color=["white"],
                        fill_color=["white"],
                    ),
                )
            ]
        )
        fig.update_layout(
            height=300,
            width=700,
            margin={"l": 20, "r": 20, "t": 25, "b": 0},
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
        )
        fig.update_layout(title_text="Most Common Referer")

        st.plotly_chart(fig, use_container_width=False)


if __name__ == "__main__":
    main()
