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
df_lookup = pd.read_csv(os.path.join('data', 'lookup.csv'))
data_load_state.text("")

st.header("General lookup board")
st.subheader("Useful for simple queries of specific ID or privacy policy to get a full audit trail")
st.write(
    """You can set multiple filters here:
    """
)

for col in df_lookup.columns:
    if is_object_dtype(df_lookup[col]):
        try:
            df_lookup[col] = pd.to_datetime(df_lookup[col])
        except Exception:
            pass
    if is_datetime64_any_dtype(df_lookup[col]):
        df_lookup[col] = df_lookup[col].dt.tz_localize(None)
df_lookup.style.set_properties(**{'background-color': 'white'})

def filter_dataframe(df_lookup: pd.DataFrame) -> pd.DataFrame:
    modify = st.checkbox("Add filters")

    if not modify:
        return df_lookup

    df_lookup = df_lookup.copy()

    #this section can be deleted
    for col in df_lookup.columns:
        if is_object_dtype(df_lookup[col]):
            try:
                df_lookup[col] = pd.to_datetime(df_lookup[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df_lookup[col]):
            df_lookup[col] = df_lookup[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df_lookup.columns)

        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")

            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df_lookup[column]) or df_lookup[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df_lookup[column].unique(),
                    default=list(df_lookup[column].unique()),
                )
                df = df_lookup[df_lookup[column].isin(user_cat_input)]

            elif is_numeric_dtype(df_lookup[column]):
                _min = float(df_lookup[column].min())
                _max = float(df_lookup[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                  f"Values for {column}",
                  min_value=_min,
                  max_value=_max,
                  value=(_min, _max),
                  step=step,
                )
                df_lookup = df_lookup[df_lookup[column].between(*user_num_input)]

            elif is_datetime64_any_dtype(df_lookup[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df_lookup[column].min(),
                        df_lookup[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df_lookup = df_lookup.loc[df_lookup[column].between(start_date, end_date)]

            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df_lookup = df_lookup[df_lookup[column].astype(str).str.contains(user_text_input)]
    return df_lookup


st.dataframe(filter_dataframe(df_lookup), width=2000, height=700)
