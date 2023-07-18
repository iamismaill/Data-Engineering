## Setting up Postgres on Docker

To set up Postgres on Docker, follow these steps:

1. Set environment variables using the `docker run` command.
   ```bash
   docker run -it \
     -e POSTGRES_USER="root" \
     -e POSTGRES_PASSWORD="root" \
     -e POSTGRES_DB="ny_taxi" \
     postgres:13
2. Enable Postgres to access a directory on the host system using the -v flag
   ```bash
   docker run -it \
     -e POSTGRES_USER="root" \
     -e POSTGRES_PASSWORD="root" \
     -e POSTGRES_DB="ny_taxi" \
     -v ($pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
     postgres:13

3. Establish communication between the host machine and the container by mapping a port using the -p
   ```bash
   docker run -it \
     -e POSTGRES_USER="root" \
     -e POSTGRES_PASSWORD="root" \
     -e POSTGRES_DB="ny_taxi" \
     -v ($pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
     -p 5432:5432 \
     postgres:13

Accessing the Database with PGCLI
1. To access the Postgres database using pgcli, follow these steps:
```bash
   !pip install pgcli
2. Launch pgcli with the following command:
```bash
   pgcli -h localhost -p 5432 -u root -d ny_taxi
Load NYC Taxi Trip Data to Postgres
   To load the NYC taxi trip data into Postgres, follow these steps:

1. Obtain the dataset from the NYC Taxi and Limousine Commission (TLC) website.
```bash
   wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet
2.Install the necessary library for handling Parquet files:
```bash
   pip install pyarrow
3.Import Pandas and read the Parquet file:
```bash
   import pandas as pd
   df = pd.read_parquet('yellow_tripdata_2023-01.parquet')
4.Create the table creation string using Pandas IO module and SQLAlchemy:
```bash
   from sqlalchemy import create_engine
   engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
   print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))
5.Insert the data into the table in chunks using Pandas' to_sql method and measure the time taken for each chunk:
```bash
   from time import time
   
   t_start = time()
   n = len(data)
   chunk_size = 100000
   
   for i in range(0, n, chunk_size):
       chunk = data[i:i+chunk_size]
       chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')
   
       t_end = time()
       print(f"Inserted another chunk and it took {t_end - t_start} seconds")










