import streamlit as st
import pandas as pd
from Healthcheck_Dashboard import credentials, schema
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

data_load_state = st.text("Loading data...")

df_users_query = "select * from " + schema + ".snowplow_web_consent_users"
df_users = pd.read_gbq(df_users_query,credentials=credentials)
data_load_state.text("")

st.header("Consent Overview by Users")
st.subheader("View the overall and latest consent interactions by user")

st.write(
    """You can set multiple filters here:
    """
)

for col in df_users.columns:
    if is_object_dtype(df_users[col]):
        try:
            df_users[col] = pd.to_datetime(df_users[col])
        except Exception:
            pass
    if is_datetime64_any_dtype(df_users[col]):
        df_users[col] = df_users[col].dt.tz_localize(None)
df_users.style.set_properties(**{'background-color': 'white'})
st.session_state['df_users'] = df_users
df = st.session_state['df_users']

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    #this section can be deleted
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)

        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")

            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]

            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                  f"Values for {column}",
                  min_value=_min,
                  max_value=_max,
                  value=(_min, _max),
                  step=step,
                )
                df = df[df[column].between(*user_num_input)]

            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]

            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]
    return df


st.dataframe(filter_dataframe(df), width=2000, height=700)
