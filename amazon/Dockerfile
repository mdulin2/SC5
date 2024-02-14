FROM ubuntu:16.04

## Setup the 'amazon' user 
RUN useradd -d /home/amazon/ -m -p amazon -s /bin/bash amazon
RUN useradd amazonPriv -s /bin/bash
RUN echo "amazon:amazon" | chpasswd
RUN chown -R root:amazon  /home/amazon

# Setup the files for the challenge
RUN apt-get update && DEBIAN_FRONTEND="noninteractive" TZ="America/New_York" apt-get -y install build-essential openssh-server vim gcc python3 git curl bsdmainutils nano tmux -y python3-pip strace
COPY amazon.c /home/amazon/amazon.c
COPY flag.txt /home/amazon/flag.txt
RUN gcc -o /home/amazon/amazon /home/amazon/amazon.c -ggdb
RUN mkdir /home/amazon/OTP 

# Compile and setup permissions
RUN chmod 6755 /home/amazon/amazon
RUN chmod 400 /home/amazon/OTP
RUN chown root:amazonPriv /home/amazon/flag.txt
RUN chmod 440 /home/amazon/flag.txt

ADD ./start.sh /start.sh
RUN chmod +x /start.sh

#ENTRYPOINT socat TCP-LISTEN:10001,reuseaddr,fork EXEC:"/amazon-challenge/amazon",pty,stderr

RUN mkdir /var/run/sshd
EXPOSE 22/tcp 
ENTRYPOINT /start.sh