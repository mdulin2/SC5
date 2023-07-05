FROM ubuntu:22.04

# Add GDB, Python, SSH, gcc and curl
RUN apt-get update -y && DEBIAN_FRONTEND="noninteractive" TZ="America/New_York" apt install openssh-server g++-multilib vim gcc python3 git curl bsdmainutils nano tmux perl -y

# Setup the users
## Setup the 'surroundings' user to login with
RUN useradd -d /home/surroundings/ -m -p surroundings -s /bin/bash surroundings
RUN echo "surroundings:surroundings" | chpasswd
RUN chown -R root:surroundings  /home/surroundings

## Setup the user that owns the flag
RUN useradd -d /home/flag_user/ -m -s /bin/bash flag_user
RUN chown -R root:flag_user  /home/flag_user


# Copy in the files
ADD hit_limit.py /home/surroundings/hit_limit.py
ADD run.c /home/surroundings/run.c
ADD ./flag.txt /home/surroundings/flag.txt
ADD ./files /home/surroundings/files/

RUN gcc /home/surroundings/run.c -o  /home/surroundings/run -m32 -ggdb -O0

# Setup the proper file for each set of exercises
RUN chown root:surroundings /home/surroundings/run
RUN chown root:flag_user /home/surroundings/flag.txt
RUN chown root:flag_user /home/surroundings/hit_limit.py

# Setup the permissions for the process. Difference between flag_user and surroundings is ability to read the 'flag'
RUN chmod 6755 /home/surroundings/run
RUN chmod 440 /home/surroundings/flag.txt
RUN chmod 744 /home/surroundings/run.c
RUN chmod 755 /home/surroundings/hit_limit.py

# SSH server startup. When launching this, specify which port that the SSH (locally port 22) will be bounded to
RUN mkdir /var/run/sshd
EXPOSE 22/tcp 
ENTRYPOINT service ssh restart && sleep 5d

