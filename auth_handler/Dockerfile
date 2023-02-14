FROM ubuntu:16.04

WORKDIR /auth_handler
RUN apt-get update && apt-get -y install build-essential gcc socat netcat python3
COPY ./flag.txt ./flag.txt
COPY ./auth_handler.py ./auth_handler.py
ENTRYPOINT socat TCP-LISTEN:10003,reuseaddr,fork EXEC:"python3 auth_handler.py",pty,stderr
