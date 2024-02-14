FROM ubuntu:16.04

# Add GDB, Python, SSH, gcc and curl
RUN apt-get update -y 
RUN DEBIAN_FRONTEND="noninteractive" TZ="America/New_York" apt install openssh-server g++-multilib vim gcc python git curl bsdmainutils nano tmux build-essential perl emacs vim -y

# Setup the users
## Setup the 'odd' user to login with
RUN useradd -d /home/odd/ -m -p odd -s /bin/bash odd
RUN echo "odd:odd" | chpasswd
RUN chown -R root:odd  /home/odd

## Setup the user that owns the flag
RUN useradd -d /home/flag_user/ -m -s /bin/bash flag_user
RUN chown -R root:flag_user  /home/flag_user


# Copy in the files
ADD odd.py /home/odd/odd.py
ADD run.c /home/odd/run.c
ADD ./flag.txt /home/odd/flag.txt

RUN gcc /home/odd/run.c -o  /home/odd/run -m32 -ggdb -O0

# Setup the proper file for each set of exercises
RUN chown root:odd /home/odd/run
RUN chown root:flag_user /home/odd/flag.txt
RUN chown root:flag_user /home/odd/odd.py

# Setup the permissions for the process. Difference between flag_user and odd is ability to read the 'flag'
RUN chmod 6755 /home/odd/run
RUN chmod 440 /home/odd/flag.txt
RUN chmod 744 /home/odd/run.c
RUN chmod 744 /home/odd/odd.py

# SSH server startup. When launching this, specify which port that the SSH (locally port 22) will be bounded to
RUN mkdir /var/run/sshd
EXPOSE 22/tcp 
ENTRYPOINT service ssh restart && sleep 5d

