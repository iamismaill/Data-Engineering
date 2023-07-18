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
To access the Postgres database using pgcli, follow these steps:
```bash
   !pip install pgcli



