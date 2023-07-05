FROM ubuntu:20.04

WORKDIR /mean_what_you_sign
RUN apt-get update && apt-get -y install build-essential gcc socat netcat python3 python3-pip
COPY ./flag.txt ./flag.txt
COPY ./mean_what_you_sign.py ./mean_what_you_sign.py
RUN pip3 install pycryptodome

ENTRYPOINT socat TCP-LISTEN:10000,reuseaddr,fork EXEC:"python3 mean_what_you_sign.py",pty,stderr
