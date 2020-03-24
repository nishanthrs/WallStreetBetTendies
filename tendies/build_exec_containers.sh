#!/bin/bash

# Build and execute containers; output logs to temp directory
sudo `which docker-compose` down -v
sudo `which docker-compose` up -d --build
sudo docker ps -a
sudo `which docker-compose` logs web > /tmp/web_docker_output.log
sudo `which docker-compose` logs sql_db > /tmp/sql_db_docker_output.log
sudo `which docker-compose` logs nosql_db > /tmp/nosql_db_docker_output.log
sudo `which docker-compose` logs nginx > /tmp/nginx_docker_output.log

# Back up data from Postgres database to Postgres container db01
sudo docker cp wsb_tendies.sql db01:/var/lib/postgresql/data
sudo docker exec db01 psql -U postgres -d wsb_tendies -f /var/lib/postgresql/data/wsb_tendies.sql > /tmp/import_db_from_host_to_container.log
sudo docker exec db01 psql -U postgres -d wsb_tendies -c "\dt"
