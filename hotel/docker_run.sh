#!/bin/bash 

sudo docker build . --tag hotel
sudo docker run --privileged -d -p 8080:8080 --cap-add=SYS_PTRACE --security-opt seccomp=unconfined -it hotel

# DEBUG version -- goes into the container automatically
docker_ps=$(sudo docker ps -q | head -n1) 
sudo docker exec -u root -it $docker_ps /bin/bash
