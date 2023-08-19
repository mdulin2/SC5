#!/bin/bash 

sudo docker build . --tag stripe || exit 
sudo docker run --privileged -d -p 5000:5000 -p 4000:4000 stripe || exit 

# DEBUG version -- goes into the container automatically
docker_ps=$(sudo docker ps -q | head -n1) 
sudo docker exec -u root -it $docker_ps /bin/bash
sudo docker kill $docker_ps
