#!/usr/bin/env python
from google.oauth2 import service_account
import pandas_gbq as pdgbq
import pandas as pd
import streamlit as st
import os


def get_data_from_bigquery(filename: str) -> pd.DataFrame:
    """Run a query against BigQuery from a file and return a dataframe with lowercase column names

    Args:
        filename (str): Path to the .sql file with the query in

    Raises:
        FileNotFoundError: When file is not found

    Returns:
        pdgbq.DataFrame: Dataframe of results
    """
    # Check for file and if it doesn't exist look for bigquery version
    if not os.path.isfile(filename):
        bespoke_filename, ext = os.path.splitext(filename)
        new_filename = bespoke_filename + '_bigquery' + ext
        if not os.path.isfile(new_filename):
            raise FileNotFoundError(f'Query file {filename} does not exist, and does not have a bigquery version.')
        else:
            filename = new_filename

    with open(filename, "r") as f:
        query = f.read()

    db_creds = st.secrets["bigquery"]
    project = db_creds["project_id"]
    dataset = db_creds["dataset"]

    query = query.replace('$1', f'`{project}`')
    query = query.replace('$2', f'`{dataset}`')
    df = pdgbq.read_gbq(query, credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"]))
    df.columns= df.columns.str.lower()
    return df


def download_data(query_file, data_file):
    df = get_data_from_bigquery(query_file)
    df.to_csv(os.path.join('data', data_file), index=False)
