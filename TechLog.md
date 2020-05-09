### Docker:
Important Points:  
Separate containers are spun up for each database dependency (e.g. PostgreSQL, MongoDB), web app itself (Django and Gunicorn), and proxy server (nginx). Thus, this app would require 4 separate containers, each with its own exposed port so that containers can communicate with each other.  
docker-compose.yml defines how each service is spun up within each container.  

Useful Commands:  
Stop and remove containers and volumes:  
```sudo `which docker-compose` down -v``` 

By default, Docker does not expose its port to other computers outside of the network.  
--publish (-p) flag exposes a port by mapping container port to its host's port.  
Ex. -p 8080:80 maps 8080 port on Docker host to TCP port 80 on Docker container (requests to Docker host on port 8080 will be redirected to port 80 on container)   
Ex. 0.0.0.0:32768->80/tcp under a container's ports means that host's 32768 port maps to container's 80 port (which is exposed).  
Each Docker container assigned an IP address for each network it's connected to.  

Commands to Build, Test, Run Container:
1. Build and run container to ensure there are no errors in config in Dockerfile and docker-compose.yml:   
```sudo `which docker-compose` up -d --build```   
Stop running containers:  
```sudo `which docker-compose` stop```  
Start running containers:  
```sudo `which docker-compose` start```  
2. Check logs/status of services defined in docker-compose.yml:  
```sudo `which docker-compose` logs <service_name>```

Commands to Push Container:  
1. Pull up a list of images:  
```sudo docker images```
2. Create a tag for a container:  
```sudo docker tag <image_id> <docker_username>/<docker_hub_repo>:<tag_name>```  
3. Push image to Docker hub with tag:  
```sudo docker push <docker_username>/<docker_hub_repo>:<tag_name>```  

Commands to Pull Container:  
```docker pull <docker_username>/<docker_hub_repo>:<tag_name>```  

Get Docker container IP address:  
```sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_name>```  

Remove exited Docker containers:  
```docker ps -a | grep "Exited" | awk '{print $1}' | xargs docker rm```  

Remove dangling Docker images:  
```docker images -q --filter "dangling=true" | xargs docker rmi```  

When running containers on another VM, make sure:  
1. Configure VM inbound port rules and permissions 
2. Add VM IP address to ALLOWED_HOSTS  
3. SCP over credential files and database backups (Postgres, Mongo)  
```scp -r credentials/ nsalina@13.64.190.69:~/WallStreetBetTendies/tendies/credentials/```  

### PostgreSQL:  
Port connections error  
Changing listen_address to 0.0.0.0 or *  

Copy data from host to container:  
```pg_dump -h localhost -U wsb_django_user wsb_tendies > /var/lib/postgresql/wsb_tendies.sql```  
```sudo docker cp /var/lib/postgresql/wsb_tendies.sql db01:/var/lib/postgresql/data```  
```sudo docker exec db01 psql -U postgres -d wsb_tendies -f /var/lib/postgresql/data/wsb_tendies.sql```  
```sudo docker exec db01 psql -U postgres -d wsb_tendies -c "\dt"```  
```docker exec -it <container> bash```   

### MongoDB:
Port connections error
Changing bindIP to 0.0.0.0 or *  

Copy data from host to container:
```mongodump -h localhost -d wsb_tendies -u mongo -p 411_wsb_tendies```
```sudo docker cp dump db02:/dump```
```sudo docker exec db02 sh -c mongorestore /dump```

Draw a diagram of Docker containers in a Ubuntu host and the request path to make sense of how they work!

### Django:
ALLOWED_HOSTS  

KEEP IN MIND THAT YOU'RE NOT EVEN USING THE DATABASE IN SETTINGS.PY SINCE YOU'RE DIRECTLY CONNECTING TO THE DATABASE VIA A LIBRARY CLIENT (pyscopg2, pymongo). SO THOSE SETTINGS ARE USELESS.

```python3 manage.py runserver $IP_ADDR:$APP_PORT```  
```python3 data_scripts/<script_to_run>```