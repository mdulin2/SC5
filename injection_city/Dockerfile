FROM ubuntu:22.04 as base

# Add GDB, Python, SSH, gcc and curl
RUN apt-get update -y && DEBIAN_FRONTEND="noninteractive" TZ="America/New_York" apt install openssh-server vim python3 git curl bsdmainutils tmux tcpdump python3-pip ffmpeg -y

# include ping
RUN apt-get install iputils-ping sqlite -y

# Start script 
COPY start.sh start.sh 
RUN chmod +x start.sh
RUN pip install flask beautifulsoup4 slimit 

RUN mkdir /flags
ADD flags /flags

# uid 1000
RUN useradd -m -p flag1 -s /bin/bash flag1
RUN chown -R flag1:flag1 /flags/flag1.txt
RUN chmod 400 /flags/flag1.txt

# uid 1001
RUN useradd -m -p flag2 -s /bin/bash flag2
RUN chown -R flag2:flag2 /flags/flag2.txt
RUN chmod 400 /flags/flag2.txt

# uid 1002
RUN useradd -m -p flag3 -s /bin/bash flag3
RUN chown -R flag3:flag3 /flags/flag3.txt
RUN chmod 400 /flags/flag3.txt

# uid 1003
RUN useradd -m -p flag4 -s /bin/bash flag4
RUN chown -R flag4:flag4 /flags/flag4.txt
RUN chmod 400 /flags/flag4.txt

# uid 1004
RUN useradd -m -p flag5 -s /bin/bash flag5
RUN chown -R flag5:flag5 /flags/flag5.txt
RUN chmod 400 /flags/flag5.txt

# uid 1005
RUN useradd -m -p flag6 -s /bin/bash flag6
RUN chown -R flag6:flag6 /flags/flag6.txt
RUN chmod 400 /flags/flag6.txt

ADD ./test_file.txt /tmp/test_file.txt
RUN chmod 777 /tmp/test_file.txt

# Frontend code
RUN mkdir /app
ADD flask_app /app

# Restrict permission to ensure that only the 'flag5' user can access this
RUN chown -R flag6:flag6 /app/search.db 
RUN chmod 700 /app/search.db 

ENTRYPOINT ["/start.sh"]
