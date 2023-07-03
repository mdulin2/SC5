FROM ubuntu:18.04

# Add GDB, Python, SSH, gcc and curl
RUN apt-get update -y && DEBIAN_FRONTEND="noninteractive" TZ="America/New_York" apt install openssh-server g++-multilib vim gcc python3 git curl bsdmainutils nano tmux -y python3-pip strace

# Install 'gef' debugger
RUN apt-get install gdb -y
RUN export LC_CTYPE=C.UTF-8
ENV LC_CTYPE "C.UTF-8" 
RUN bash -c "$(curl -fsSL https://gef.blah.cat/sh)"

# Setup the users
## Setup the 'firsty' user 
RUN useradd -d /home/firsty/ -m -p firsty -s /bin/bash firsty
RUN useradd firstyPriv -s /bin/bash
RUN echo "firsty:firsty" | chpasswd
RUN chown -R root:firsty  /home/firsty

## Setup the 'dead' user 
RUN useradd -d /home/dead/ -m -p dead -s /bin/bash dead
RUN echo "dead:dead" | chpasswd
RUN useradd deadPriv -s /bin/sh
RUN chown -R root:dead  /home/dead

## Setup the 'killPtr' user 
RUN useradd -d /home/killPtr/ -m -p killPtr -s /bin/bash killPtr
RUN echo "killPtr:killPtr" | chpasswd
RUN useradd killPtrPriv -s /bin/sh
RUN chown -R root:killPtr  /home/killPtr

## Setup the 'corruptRet' user 
RUN useradd -d /home/corruptRet/ -m -p corruptRet -s /bin/bash corruptRet
RUN echo "corruptRet:corruptRet" | chpasswd
RUN useradd corruptRetPriv -s /bin/sh
RUN chown -R root:corruptRet  /home/corruptRet

## Setup the 'execStack' user 
RUN useradd -d /home/execStack/ -m -p execStack -s /bin/bash execStack
RUN useradd execStackPriv -s /bin/sh
RUN echo "execStack:execStack" | chpasswd
RUN chown -R execStack:execStack  /home/execStack

# Flag files
ADD ./flag1.txt /home/firsty/flag.txt
ADD ./flag2.txt /home/dead/flag.txt
ADD ./flag3.txt /home/killPtr/flag.txt
ADD ./flag4.txt /home/corruptRet/flag.txt
ADD ./flag5.txt /home/execStack/flag.txt

ADD ./start.sh /start.sh
RUN chmod +x /start.sh

# Copy in the files
ADD firsty.c /home/firsty/firsty.c
ADD dead.c /home/dead/dead.c
ADD killPtr.c /home/killPtr/killPtr.c
ADD corruptRet.c /home/corruptRet/corruptRet.c
ADD execStack.c /home/execStack/execStack.c

# Compile the code for these challenges
RUN gcc /home/firsty/firsty.c -o /home/firsty/firsty -z execstack -O0 -ggdb -m32 -fno-stack-protector -no-pie
RUN gcc /home/dead/dead.c -o /home/dead/dead -z execstack -O0 -ggdb -m32 -fno-stack-protector -no-pie
RUN gcc /home/killPtr/killPtr.c -o /home/killPtr/killPtr -z execstack -O0 -ggdb -m32 -fno-stack-protector -no-pie
RUN gcc /home/corruptRet/corruptRet.c -o /home/corruptRet/corruptRet -z execstack -O0 -ggdb -m32 -fno-stack-protector -no-pie
RUN gcc /home/execStack/execStack.c -o /home/execStack/execStack -z execstack -O0 -ggdb -m32 -fno-stack-protector -no-pie


# Setup the proper file for each set of exercises
RUN chown root:firsty /home/firsty/firsty
RUN chown root:firstyPriv /home/firsty/flag.txt
RUN chmod 6755 /home/firsty/firsty
RUN chmod 440 /home/firsty/flag.txt
RUN chmod 744 /home/firsty/firsty.c

RUN chown root:dead /home/dead/dead
RUN chown root:deadPriv /home/dead/flag.txt
RUN chmod 6755 /home/dead/dead
RUN chmod 440 /home/dead/flag.txt
RUN chmod 744 /home/dead/dead.c

RUN chown root:killPtr /home/killPtr/killPtr
RUN chown root:killPtrPriv /home/killPtr/flag.txt
RUN chmod 6755  /home/killPtr/killPtr
RUN chmod 440 /home/killPtr/flag.txt
RUN chmod 744 /home/killPtr/killPtr.c

RUN chown root:corruptRet /home/corruptRet/corruptRet
RUN chown root:corruptRetPriv /home/corruptRet/flag.txt
RUN chmod 6755 /home/corruptRet/corruptRet
RUN chmod 440 /home/corruptRet/flag.txt
RUN chmod 744 /home/corruptRet/corruptRet.c

RUN chown root:execStack /home/execStack/execStack
RUN chown root:execStackPriv /home/execStack/flag.txt
RUN chmod 6755 /home/execStack/execStack
RUN chmod 440 /home/execStack/flag.txt
RUN chmod 744 /home/execStack/execStack.c

# Setup GDB properly for all of the other users
RUN chmod 755 /root/.gef-*
RUN cp /root/.gef-* /home/killPtr/
RUN cp /root/.gef-* /home/firsty/
RUN cp /root/.gef-* /home/dead/
RUN cp /root/.gef-* /home/corruptRet/
RUN cp /root/.gef-* /home/execStack/

RUN cp /root/.gdbinit /home/killPtr/.gdbinit
RUN cp /root/.gdbinit /home/firsty/.gdbinit
RUN cp /root/.gdbinit /home/dead/.gdbinit
RUN cp /root/.gdbinit /home/corruptRet/.gdbinit
RUN cp /root/.gdbinit /home/execStack/.gdbinit

# SSH server startup. When launching this, specify which port that the SSH (locally port 22) will be bounded to
RUN mkdir /var/run/sshd
EXPOSE 22/tcp 
ENTRYPOINT /start.sh

