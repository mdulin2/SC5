FROM ubuntu:16.04

# Add GDB, Python, SSH, gcc and curl
RUN apt-get update -y && DEBIAN_FRONTEND="noninteractive" TZ="America/New_York" apt install openssh-server g++-multilib vim gdb gcc python git curl bsdmainutils nano tmux perl tcpdump -y

# Setup the users
## Setup the 'firsty' user 
RUN useradd -d /home/error/ -m -p error -s /bin/bash error
RUN echo "error:error" | chpasswd
RUN chown -R root:error  /home/error

# Copy in the files
ADD error_code.c /home/error/error_code.c

# Compile the code for this challenge
RUN gcc /home/error/error_code.c -o /home/error/error_code -O0 -ggdb -no-pie

ADD ./flag.txt /home/error/flag.txt

# Setup the proper file for each set of exercises
RUN chown root:error /home/error/error_code
RUN chown root:error /home/error/flag.txt
RUN chmod 4755 /home/error/error_code
RUN chmod 400 /home/error/flag.txt
RUN chmod 744 /home/error/error_code.c

# SSH server startup. When launching this, specify which port that the SSH (locally port 22) will be bounded to
RUN mkdir /var/run/sshd
EXPOSE 22/tcp 
ENTRYPOINT service ssh restart && sleep 5d

