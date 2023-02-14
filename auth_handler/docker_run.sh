#!/bin/bash 

sudo docker build . --tag auth_handler
sudo docker run -d -p 10003:10003 -it auth_handler

# DEBUG version -- goes into the container automatically
docker_ps=$(sudo docker ps -q | head -n1) 
sudo docker exec -u root -it $docker_ps /bin/bash
