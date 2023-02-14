#!/usr/bin/env python
import snowflake.connector
import pandas as pd
import streamlit as st
import os as os

# Perform query.
def get_data_from_snowflake(filename: str) -> pd.DataFrame:
    """Run a query against Snowflake from a file and return a dataframe with lowercase column names

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
        new_filename = bespoke_filename + '_snowflake' + ext
        if not os.path.isfile(new_filename):
            raise FileNotFoundError(f'Query file {filename} does not exist, and does not have a snowflake version.')
        else:
            filename = new_filename


    with open(filename, "r") as f:
        query = f.read()

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
    return df



def download_data(query_file, data_file):
    df = get_data_from_snowflake(query_file)
    df.to_csv(os.path.join('data', data_file), index=False)
