#!/bin/bash 

sudo docker build . --tag mean_what_you_sign
sudo docker run --privileged -d -p 10000:10000 --cap-add=SYS_PTRACE --security-opt seccomp=unconfined -it mean_what_you_sign

# DEBUG version -- goes into the container automatically
docker_ps=$(sudo docker ps -q | head -n1) 
sudo docker exec -u root -it $docker_ps /bin/bash
