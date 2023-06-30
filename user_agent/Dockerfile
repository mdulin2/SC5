FROM ubuntu:22.04 as base

# Add GDB, Python, SSH, gcc and curl
RUN apt-get update -y && DEBIAN_FRONTEND="noninteractive" TZ="America/New_York" apt install openssh-server vim gdb gcc python3 curl bsdmainutils tmux  python3-pip -y

# Start script 
COPY start.sh start.sh 
RUN chmod +x start.sh
RUN pip install flask

ADD flag.txt /flag.txt

# Frontend code
RUN mkdir /frontend
ADD frontend /frontend

# Backend code
RUN mkdir /backend
ADD backend /backend

ENTRYPOINT ["/start.sh"]