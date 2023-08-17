#!/bin/bash 

sudo docker build . --tag stripe || exit 
sudo docker run --privileged -d -p 5000:5000 -p 3000:3000 stripe || exit 

# DEBUG version -- goes into the container automatically
docker_ps=$(sudo docker ps -q | head -n1) 
sudo docker exec -u root -it $docker_ps /bin/bash
