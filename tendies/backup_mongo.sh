#!/bin/bash

# Backup data from Mongo host to Mongo container 
echo "----------- BACKING UP MONGO DATA FROM DOCKER HOST ----------------"
sudo docker cp ../mongo_dump db02:/dump
sudo docker exec db02 sh -c mongorestore /dump