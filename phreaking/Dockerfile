FROM ubuntu:22.04 as base

# Add GDB, Python, SSH, gcc and curl
RUN apt-get update -y 
RUN DEBIAN_FRONTEND="noninteractive" TZ="America/New_York" apt install openssh-server vim gdb gcc python3 git curl bsdmainutils tmux tcpdump sqlite3 python3-pip ffmpeg nginx -y 

# Start script 
COPY start.sh start.sh 
RUN chmod +x start.sh
RUN pip install flask scipy websockets

# Frontend code
RUN mkdir /frontend
ADD frontend /frontend

# Backend code
RUN mkdir /backend
ADD backend /backend

# Generate an SSL cert
COPY nginx.conf /etc/nginx/sites-enabled/default
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx-selfsigned.key -out nginx-selfsigned.crt -subj "/C=PE/ST=Lima/L=Lima/O=Acme Inc. /OU=IT Department/CN=acme.com"
RUN mkdir /etc/nginx/ssl/
RUN cp nginx-selfsigned.crt /etc/nginx/ssl/nginx-selfsigned.crt
RUN cp nginx-selfsigned.key /etc/nginx/ssl/nginx-selfsigned.key

ENTRYPOINT ["/start.sh"]
