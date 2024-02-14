#!/bin/bash 

sudo docker build . --tag injection_city
sudo docker run --privileged -d -p 5001:5001 -it injection_city

# DEBUG version -- goes into the container automatically
docker_ps=$(sudo docker ps -q | head -n1) 
sudo docker exec -u root -it $docker_ps /bin/bash
