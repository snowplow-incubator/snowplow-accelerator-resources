#!/usr/bin/env python
from google.oauth2 import service_account
import pandas_gbq as pdgbq
import snowflake.connector
import pandas as pd
import streamlit as st
import os as os

# Perform query.
def get_data_from_warehouse(filename: str, warehouse: str) -> pd.DataFrame:
    """Run a query against a warehouse from a file and return a dataframe with lowercase column names

    Args:
        filename (str): Path to the .sql file with the query in

    Raises:
        FileNotFoundError: When file is not found

    Returns:
        pd.DataFrame: Dataframe of results
    """

    # Check for file and if it doesn't exist look for bigquery version
    if not os.path.isfile(filename):
        bespoke_filename, ext = os.path.splitext(filename)
        new_filename = bespoke_filename + f'_{warehouse}' + ext
        if not os.path.isfile(new_filename):
            raise FileNotFoundError(f'Query file {filename} does not exist, and does not have a {warehouse} version.')
        else:
            filename = new_filename


    with open(filename, "r") as f:
        query = f.read()
    if warehouse == 'snowflake':
        db_creds = st.secrets["snowflake"]
        user = db_creds["user"]
        password = db_creds["password"]
        account = db_creds["account"]
        database = db_creds["database"]
        role = db_creds["role"]
        warehouse = db_creds["warehouse"]
        schema = db_creds["schema"]

        conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
            database=database,
            role=role,
            warehouse=warehouse
        )

        query = query.replace('$1',f'"{database}"')
        query = query.replace('$2', f'"{schema}"')

        cs = conn.cursor()
        try:
            cs.execute(query)
            print('Results from query obtained')
            column_names = [desc[0].lower() for desc in cs.description]
            df = pd.DataFrame(cs.fetchall(), columns=column_names)
            print('Data stored in dataframe')
        finally:
            cs.close()
        conn.close()
    elif warehouse == 'bigquery':
        db_creds = st.secrets["bigquery"]
        project = db_creds["project_id"]
        dataset = db_creds["dataset"]

        query = query.replace('$1', f'`{project}`')
        query = query.replace('$2', f'`{dataset}`')
        df = pdgbq.read_gbq(query, credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"]))
        df.columns= df.columns.str.lower()

    return df



def download_data(query_file, data_file, warehouse):
    df = get_data_from_warehouse(query_file, warehouse)
    df.to_csv(os.path.join('data', data_file), index=False)


def run_download_data(warehouse: str, data_sources: list[tuple]):
    data_load_state = st.text("Downloading data...")

    for query, name in data_sources:
        download_data(os.path.join('queries', f'{query}.sql'), f'{name}.csv', warehouse.lower())

    data_load_state.text("")
    st.experimental_rerun()
