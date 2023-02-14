#!/bin/bash 

sudo docker build . --tag gradebook
sudo docker run -d -p 80:80 -it gradebook

# DEBUG version -- goes into the container automatically
docker_ps=$(sudo docker ps -q | head -n1) 
sudo docker exec -u root -it $docker_ps /bin/bash
