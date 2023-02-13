#!/usr/bin/env python
import snowflake.connector
import pandas as pd
import streamlit as st

WAREHOUSE = "snowflake"

# Perform query.
def get_data_from_snowflake(filename):
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

    query = query.replace('$1', database)
    query = query.replace('$2', schema)

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


def get_data(query_file):
    if WAREHOUSE == "snowflake":
        df = get_data_from_snowflake(query_file)

    return df
