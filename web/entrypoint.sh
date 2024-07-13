#!/bin/bash
set -e

# Copy the custom pg_hba.conf file
cp /custom_pg_hba.conf /var/lib/postgresql/data/pg_hba.conf

# Uncomment ssl = off in postgresql.conf
sed -i 's/#ssl = off/ssl = off/' /var/lib/postgresql/data/postgresql.conf

# Start the PostgreSQL server
docker-entrypoint.sh postgres