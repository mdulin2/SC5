#!/bin/bash 

sudo docker build . --tag phreaking || exit 1
sudo docker run --privileged -d -p 8000:8000 -p 8001:8001 -p 80:80 -p 443:443 -p 3000:3000 -it phreaking || exit 1

# DEBUG version -- goes into the container automatically
docker_ps=$(sudo docker ps -q | head -n1) 
sudo docker exec -u root -it $docker_ps /bin/bash
sudo docker kill $docker_ps
