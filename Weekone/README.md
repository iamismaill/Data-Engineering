## Setting up Postgres on Docker

To set up Postgres on Docker, follow these steps:

1. Set environment variables using the `docker run` command.
   ```bash
   docker run -it \
     -e POSTGRES_USER="root" \
     -e POSTGRES_PASSWORD="root" \
     -e POSTGRES_DB="ny_taxi" \
     postgres:13
2. Enable Postgres to access a directory on the host system using the -v flag.

docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ($pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  postgres:13
