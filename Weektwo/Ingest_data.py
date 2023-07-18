import pandas as pd
from time import time
from sqlalchemy import create_engine
import argparse
import os

from prefect import flow, task

@task(log_prints=True, retries=3)
def ingest_data(params):
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
    data = pd.read_parquet(parquet_name)
    data.head(0).to_sql(name=table, con=engine, if_exists='replace', schema=None)

    t_start = time()
    n = len(data)
    chunk_size = 100000

    for i in range(0, n, chunk_size):
        chunk = data[i:i+chunk_size]  # Get the chunk of data using indexing
        chunk.to_sql(name=table, con=engine, if_exists='append', schema=None)
        t_end = time()
        print(f"Inserted all chunks, took {t_end - t_start} seconds")
    
    print("Finished ingesting data into the PostgreSQL database")
@flow(name ='Ingest Flow')
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
    ingest_data(args)

if __name__ == '__main__':
    main_flow()

 
