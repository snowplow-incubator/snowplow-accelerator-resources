from utils.connect import get_data, connect_to_snowflake, disconnect_from_snowflake
import streamlit as st
import plotly.graph_objects as go
from utils.countries import data_by_country


def main():
    st.set_page_config(layout="wide", page_title="Sessions")

    st.title("Snowplow Web Insights")

    data_load_state = st.text("Loading data...")
    cs, cnx = connect_to_snowflake()
    num_sessions_by_day = get_data(cs, "queries/sessions/num_sessions_by_day.sql")
    num_sessions = get_data(cs, "queries/sessions/num_sessions.sql")

    session_duration_by_day = get_data(cs, "queries/sessions/avg_duration_by_day.sql")
    session_duration = get_data(cs, "queries/sessions/avg_duration.sql")

    sessions_by_country = get_data(cs, "queries/sessions/sessions_by_geo.sql")
    sessions_by_device = get_data(cs, "queries/sessions/sessions_by_device.sql")

    total_users = get_data(cs, "queries/users/number_of_users.sql")

    pageviews_by_day = get_data(cs, "queries/pageviews/pageviews_by_day.sql")
    pageviews_by_page = get_data(cs, "queries/pageviews/pageviews_by_page.sql")
    pageviews_by_referer = get_data(cs, "queries/pageviews/referer.sql")

    bounce_rate_by_day = get_data(cs, "queries/sessions/bounce_rate_by_day.sql")
    bounce_rate = get_data(cs, "queries/sessions/bounce_rate.sql")

    disconnect_from_snowflake(cs, cnx)

    data_load_state.text("")

    st.subheader("Summary")

    col1, col2, col3 = st.columns([1, 3, 2])

    with col1:
        st.metric(
            value="{0:,.0f}".format(num_sessions["NUMBER_OF_SESSIONS"][0]),
            label="Total Sessions",
        )
        st.metric(
            value=str(session_duration["AVERAGE_SESSION_ENGAGED_TIME_IN_S"][0]) + "s",
            label="Average Session Len",
        )
        st.metric(
            value="{0:,.0f}".format(total_users["NUMBER_OF_USERS"][0]),
            label="Total Users",
        )

    with col2:
        sessions_iso3 = data_by_country(sessions_by_country)

        fig = go.Figure(
            data=go.Choropleth(
                locations=sessions_iso3["ISO_3"],
                z=sessions_iso3["NUMBER_OF_SESSIONS"],
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
                    labels=sessions_by_device["DEVICE_FAMILY"],
                    values=sessions_by_device["NUMBER_OF_SESSIONS"],
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
                    x=num_sessions_by_day["DATE"],
                    y=num_sessions_by_day["NUMBER_OF_SESSIONS"],
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
                    x=session_duration_by_day["DATE"],
                    y=session_duration_by_day["AVG_ENGAGED_TIME"],
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
                    x=bounce_rate_by_day["DATE"],
                    y=bounce_rate_by_day["BOUNCERATE"],
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
                    x=pageviews_by_day["DATE"],
                    y=pageviews_by_day["NUMBER_OF_PAGEVIEWS"],
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
                            pageviews_by_page["PAGE_TITLE"],
                            pageviews_by_page["NUMBER_OF_PAGEVIEWS"],
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
                            pageviews_by_referer["REFR_URLHOST"],
                            pageviews_by_referer["NUMBER_OF_PAGEVIEWS"],
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
