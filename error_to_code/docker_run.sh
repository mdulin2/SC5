#!/bin/bash 

sudo docker build . --tag error_to_code
sudo docker run -d -p 2223:22 --cap-add=SYS_PTRACE -it error_to_code

# DEBUG version -- goes into the container automatically
docker_ps=$(sudo docker ps -q | head -n1) 
sudo docker exec -u root -it $docker_ps /bin/bash
