import pandas as pd
from time import time
from sqlalchemy import create_engine
import argparse
import os
from prefect.tasks import task_input_hash
from datetime import timedelta
from prefect import flow, task

@task(log_prints=True, tags=["extract"], cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_data(url):
    print("Extracting the data ")
    if url.endswith('.parquet'):
        parquet_name = 'output.parquet'
    else:
        parquet_name = 'output.parquet1'

    os.system(f"wget {url} -O {parquet_name}")
    data = pd.read_parquet(parquet_name)

    return data


@task(log_prints=True)
def transform(data):
    print(f"pre: missing passenger count: {data['passenger_count'].isin([0]).sum()}")
    data = data[data['passenger_count'] != 0]
    print(f"post: missing passenger count: {data['passenger_count'].isin([0]).sum()}")
    return data


def ingest_data(params, data):
    print("Succesfuly extracted")
    print("Ingesting the data")
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table = params.table_name
    url = params.url

    if url.endswith('.parquet'):
        parquet_name = 'output.parquet'
    else:
        parquet_name = 'output.parquet1'

    os.system(f"wget {url} -O {parquet_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    data.head(0).to_sql(name=table, con=engine, if_exists='replace', schema=None)

    t_start = time()
    n = len(data)
    chunk_size = 100000

    for i in range(0, n, chunk_size):
        chunk = data[i:i+chunk_size]
        chunk.to_sql(name=table, con=engine, if_exists='append', schema=None)
        t_end = time()
        print(f"Inserted all chunks, took {t_end - t_start} seconds")

    print("Finished ingesting data into the PostgreSQL database")


@flow(name='Ingest Flow')
def main_flow():
    parser = argparse.ArgumentParser(description='Ingest Parquet data into PostgreSQL')

    parser.add_argument('--user', required=True, help='user name for PostgreSQL')
    parser.add_argument('--password', required=True, help='password for PostgreSQL')
    parser.add_argument('--host', required=True, help='host for PostgreSQL')
    parser.add_argument('--port', required=True, help='port for PostgreSQL')
    parser.add_argument('--db', required=True, help='database name for PostgreSQL')
    parser.add_argument('--table_name', required=True, help='name of the table where I will write the results to')
    parser.add_argument('--url', required=True, help='URL of the Parquet file')

    args = parser.parse_args()
    raw_data = extract_data(args.url)
    transformed_data = transform(raw_data)
    ingest_data(args, transformed_data)


if __name__ == '__main__':
    main_flow()
