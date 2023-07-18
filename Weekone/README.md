## Setting up Postgres on Docker

### To set up Postgres on Docker, follow these steps:

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

#### Accessing the Postgres Database with pgcli

To access the Postgres database using pgcli, follow these steps:

1. Install pgcli by running the following command:

   ```bash
   pip install pgcli

2. Launch pgcli with the following command:
   ```bash
    pgcli -h localhost -p 5432 -u root -d ny_taxi

