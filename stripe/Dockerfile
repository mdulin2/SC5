FROM ubuntu:20.04 as base

# Add GDB, Python, SSH, gcc and curl
RUN apt-get update -y && DEBIAN_FRONTEND="noninteractive" TZ="America/New_York" apt install vim gcc python3 git curl bsdmainutils tmux sqlite3 python3-pip  -y
RUN DEBIAN_FRONTEND="noninteractive" TZ="America/New_York" apt install -y nodejs npm

# Start script 
COPY start.sh start.sh 
RUN chmod +x start.sh

# Backend code
RUN mkdir /backend
ADD backend /backend

# Frontend code
RUN mkdir /frontend
ADD frontend /frontend

ENTRYPOINT ["/start.sh"]
