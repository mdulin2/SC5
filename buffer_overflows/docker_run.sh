#!/bin/bash 

sudo docker build . --tag stack_overflows
sudo docker run --privileged -d -p 2222:22 --cap-add=SYS_PTRACE --security-opt seccomp=unconfined -it stack_overflows

# DEBUG version -- goes into the container automatically
docker_ps=$(sudo docker ps -q | head -n1) 
sudo docker exec -u root -it $docker_ps /bin/bash
