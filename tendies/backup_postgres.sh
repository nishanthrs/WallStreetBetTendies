#!/bin/bash

# Back up data from Postgres database to Postgres container db01

echo "----------- BACKING UP POSTGRES DATA FROM DOCKER HOST -------------"
# TODO: In case container runs on diff host as master db, add command pg_dump to dump data on remote machine and scp it over to host
sudo docker cp ../postgres_dump/wsb_tendies.sql db01:/var/lib/postgresql/data
sudo docker exec db01 psql -U postgres -d wsb_tendies -f /var/lib/postgresql/data/wsb_tendies.sql > /tmp/import_db_from_host_to_container.log
sudo docker exec db01 psql -U postgres -d wsb_tendies -c "\dt"