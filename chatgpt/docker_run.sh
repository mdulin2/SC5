#!/bin/bash 

sudo docker build . --tag chatgpt-chal

mkdir -p logs
touch logs/record.log
sudo docker run -d -p 8083:8083 -v $(pwd)/logs:/logs -it chatgpt-chal
