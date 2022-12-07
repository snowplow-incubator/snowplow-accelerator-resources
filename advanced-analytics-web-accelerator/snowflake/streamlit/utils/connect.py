#!/usr/bin/env python
import snowflake.connector
import streamlit as st
import pandas as pd

WAREHOUSE = "snowflake"

def connect_to_snowflake():
    db_creds = st.secrets["snowflake"]
    cnx = snowflake.connector.connect(
        user=db_creds["user"],
        password=db_creds["password"],
        account=db_creds["account"],
        database=db_creds["database"],
        warehouse=db_creds["warehouse"],
        role=db_creds["role"],
        schema=db_creds["schema"]
    )

    cs = cnx.cursor()
    print("Connected to Snowflake")

    return cs, cnx


def get_data_from_snowflake(cs, filename):
    with open(filename, "r") as f:
        query = f.read()

        cs.execute(query)
        column_names = [desc[0] for desc in cs.description]
        df = pd.DataFrame(cs.fetchall(), columns=column_names)
    return df

def disconnect_from_snowflake(cs, cnx):
    cs.close()
    cnx.close()

def get_data(cs, query):
    if WAREHOUSE == "snowflake":
        df = get_data_from_snowflake(cs, query)

    return df
