FROM ubuntu:20.04

WORKDIR /miner
RUN apt-get update && apt-get -y install build-essential gcc socat netcat python3 python3-pip
RUN pip3 install pycryptodome flask

COPY ./flag.txt ./flag.txt
COPY ./server.py ./server.py

ENTRYPOINT python3 server.py
