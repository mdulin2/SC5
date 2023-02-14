#!/bin/bash 

sudo docker build . --tag amazon
sudo docker run -d -p 10001:10001 -it amazon

# DEBUG version -- goes into the container automatically
docker_ps=$(sudo docker ps -q | head -n1) 
sudo docker exec -u root -it $docker_ps /bin/bash
