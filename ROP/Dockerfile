FROM ubuntu:22.04 as base

# Add GDB, Python, SSH, gcc and curl
RUN apt-get update -y && DEBIAN_FRONTEND="noninteractive" TZ="America/New_York" apt install vim gcc python3 curl bsdmainutils tmux python3-pip wget -y

# Start script 
COPY start.sh start.sh 
RUN chmod +x start.sh
RUN pip install flask js2py flask-cors

ADD flag.txt /flag.txt

# Frontend code
RUN mkdir /frontend
ADD frontend /frontend

# Backend code
RUN mkdir /backend
ADD backend /backend

ENTRYPOINT ["/start.sh"]