#!/bin/bash

# Build and execute containers; output logs to temp directory
echo "----------- BUILDING AND EXECUTING CONTAINERS ---------------"
sudo `which docker-compose` down -v
sudo `which docker-compose` up -d --build
sudo docker ps -a
sudo `which docker-compose` logs web > /tmp/web_docker_output.log
sudo `which docker-compose` logs sql_db > /tmp/sql_db_docker_output.log
sudo `which docker-compose` logs nosql_db > /tmp/nosql_db_docker_output.log
sudo `which docker-compose` logs nginx > /tmp/nginx_docker_output.log

./backup_postgres.sh
./backup_mongo.sh