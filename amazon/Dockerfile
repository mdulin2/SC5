FROM ubuntu:16.04

WORKDIR /amazon-challenge
RUN apt-get update && apt-get -y install build-essential gcc socat netcat
COPY ./amazon.c ./amazon.c
COPY ./flag.txt ./flag.txt
COPY ./amazon ./amazon
RUN mkdir ./OTP 
#CMD gcc -o amazon amazon.c -ggdb
ENTRYPOINT socat TCP-LISTEN:10001,reuseaddr,fork EXEC:"/amazon-challenge/amazon",pty,stderr
