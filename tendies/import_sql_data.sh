#!/bin/bash

sudo docker cp wsb_tendies.sql db01:/var/lib/postgresql/data
sudo docker exec db01 psql -U postgres -d wsb_tendies -f /var/lib/postgresql/data/wsb_tendies.sql
sudo docker exec db01 psql -U postgres -d wsb_tendies -c "\dt"