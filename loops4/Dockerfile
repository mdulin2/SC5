FROM sagemath/sagemath

# Add GDB, Python, SSH, gcc and curl
USER root
RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y openssh-server

RUN chmod +x /home/sage
RUN chmod +x /home/sage/sage

WORKDIR /usr/bin

COPY src/ecc_loops.sh .
RUN chmod +x ecc_loops.sh
WORKDIR /usr/share/learning_rsa

COPY src/ecc_loops.py .

RUN useradd -m -s /usr/bin/ecc_loops.sh -p '' loops4

RUN sed -i '/#PasswordAuthentication yes/c\PasswordAuthentication yes' /etc/ssh/sshd_config
RUN sed -i '/#PermitEmptyPasswords no/c\PermitEmptyPasswords yes' /etc/ssh/sshd_config
RUN sed -i '/UsePAM yes/c\UsePAM no' /etc/ssh/sshd_config

RUN mkdir /var/run/sshd
EXPOSE 22/tcp
CMD [ "/usr/sbin/sshd", "-D" ]


