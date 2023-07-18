## Setting up Postgres on Docker

To set up Postgres on Docker, follow these steps:

1. Set environment variables using the `docker run` command.
   ```bash
   docker run -it \
     -e POSTGRES_USER="root" \
     -e POSTGRES_PASSWORD="root" \
     -e POSTGRES_DB="ny_taxi" \
     postgres:13
