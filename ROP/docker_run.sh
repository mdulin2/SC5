#!/bin/bash 

sudo docker build . --tag javascript_rop
sudo docker run --privileged -d -p 3010:3010 -p 8000:8000 -it javascript_rop

# DEBUG version -- goes into the container automatically
docker_ps=$(sudo docker ps -q | head -n1) 
sudo docker exec -u root -it $docker_ps /bin/bash
