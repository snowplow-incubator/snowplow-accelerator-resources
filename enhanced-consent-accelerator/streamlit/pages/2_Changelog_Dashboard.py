import streamlit as st
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
from utils.connect import run_download_data
import os


data_sources = st.session_state['data_sources']
_WAREHOUSE = st.session_state['_WAREHOUSE']

# Button to re-run and load the data
if st.button('Refresh Data'):
    run_download_data(_WAREHOUSE, data_sources)

# Load the data from local files
data_load_state = st.text("Loading data...")
df_changelog = pd.read_csv(os.path.join('data', 'changelog.csv'))
data_load_state.text("")

st.header("Changelog Dashboard")
st.subheader("View the changes happening in user consent preference over specific period of time. List of IDs and their changed statuses from original value into new actual")
st.write(
    """You can set multiple filters here:
    """
)

for col in df_changelog.columns:
    if is_object_dtype(df_changelog[col]):
        try:
            df_changelog[col] = pd.to_datetime(df_changelog[col])
        except Exception:
            pass
    if is_datetime64_any_dtype(df_changelog[col]):
        df_changelog[col] = df_changelog[col].dt.tz_localize(None)
df_changelog.style.set_properties(**{'background-color': 'white'})

def filter_dataframe(df_changelog: pd.DataFrame) -> pd.DataFrame:
    modify = st.checkbox("Add filters")

    if not modify:
        return df_changelog

    df_changelog = df_changelog.copy()

    #this section can be deleted
    for col in df_changelog.columns:
        if is_object_dtype(df_changelog[col]):
            try:
                df_changelog[col] = pd.to_datetime(df_changelog[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df_changelog[col]):
            df_changelog[col] = df_changelog[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df_changelog.columns)

        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")

            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df_changelog[column]) or df_changelog[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df_changelog[column].unique(),
                    default=list(df_changelog[column].unique()),
                )
                df = df_changelog[df_changelog[column].isin(user_cat_input)]

            elif is_numeric_dtype(df_changelog[column]):
                _min = float(df_changelog[column].min())
                _max = float(df_changelog[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                  f"Values for {column}",
                  min_value=_min,
                  max_value=_max,
                  value=(_min, _max),
                  step=step,
                )
                df_changelog = df_changelog[df_changelog[column].between(*user_num_input)]

            elif is_datetime64_any_dtype(df_changelog[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df_changelog[column].min(),
                        df_changelog[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df_changelog = df_changelog.loc[df_changelog[column].between(start_date, end_date)]

            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df_changelog = df_changelog[df_changelog[column].astype(str).str.contains(user_text_input)]
    return df_changelog


st.dataframe(filter_dataframe(df_changelog), width=2000, height=700)
