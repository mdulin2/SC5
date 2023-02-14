FROM ubuntu:18.04

# Add GDB, Python, SSH, gcc and curl
RUN apt-get update -y && DEBIAN_FRONTEND="noninteractive" TZ="America/New_York" apt install openssh-server g++-multilib vim gcc python git curl bsdmainutils nano tmux perl -y

# Setup the users
## Setup the 'no_char' user to login with
RUN useradd -d /home/no_char/ -m -p no_char -s /bin/bash no_char
RUN echo "no_char:no_char" | chpasswd
RUN chown -R root:no_char  /home/no_char

## Setup the user that owns the flag
RUN useradd -d /home/flag_user/ -m -s /bin/bash flag_user
RUN chown -R root:flag_user  /home/flag_user


# Copy in the files
ADD no_char.py /home/no_char/no_char.py
ADD run.c /home/no_char/run.c
ADD ./flag.txt /home/no_char/flag.txt

RUN gcc /home/no_char/run.c -o  /home/no_char/run -m32 -ggdb -O0

# Setup the proper file for each set of exercises
RUN chown root:no_char /home/no_char/run
RUN chown root:flag_user /home/no_char/flag.txt
RUN chown root:flag_user /home/no_char/no_char.py

# Setup the permissions for the process. Difference between flag_user and no_char is ability to read the 'flag'
RUN chmod 6755 /home/no_char/run
RUN chmod 440 /home/no_char/flag.txt
RUN chmod 744 /home/no_char/run.c
RUN chmod 744 /home/no_char/no_char.py

# SSH server startup. When launching this, specify which port that the SSH (locally port 22) will be bounded to
RUN mkdir /var/run/sshd
EXPOSE 22/tcp 
ENTRYPOINT service ssh restart && sleep 5d

