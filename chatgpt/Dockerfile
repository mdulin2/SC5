FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    apt-get install -y wget python3-pip python3-dev && \
    apt-get install -y libfreetype6 libfreetype6-dev && \
    apt-get install -y libfontconfig1 libfontconfig1-dev
RUN apt-get install -y nginx

# We copy just the requirements.txt first to leverage Docker cache
COPY ./server/requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY ./server /app

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

CMD ["flask", "run", "--host=0.0.0.0", "--port=8083"]
