#!/bin/bash 

sudo docker build . --tag user_agent
sudo docker run --privileged -d -p 8000:8000 -it user_agent

# DEBUG version -- goes into the container automatically
docker_ps=$(sudo docker ps -q | head -n1) 
sudo docker exec -u root -it $docker_ps /bin/bash
