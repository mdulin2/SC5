#!/bin/bash 

sudo docker build . --tag odd
sudo docker run -d -p 2228:22 --cap-add=SYS_PTRACE -it odd

# DEBUG version -- goes into the container automatically
docker_ps=$(sudo docker ps -q | head -n1) 
sudo docker exec -u root -it $docker_ps /bin/bash
