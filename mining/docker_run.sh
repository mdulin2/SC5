#!/bin/bash 

sudo docker build . --tag miner
sudo docker run --privileged -d -p 10001:10001 --cap-add=SYS_PTRACE --security-opt seccomp=unconfined -it miner

# DEBUG version -- goes into the container automatically
docker_ps=$(sudo docker ps -q | head -n1) 
sudo docker exec -u root -it $docker_ps /bin/bash
