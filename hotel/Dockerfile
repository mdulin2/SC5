FROM python:3.8

RUN mkdir /app
WORKDIR /app

COPY ./cart.html ./cart.html 
COPY ./list.html ./list.html 
COPY ./img ./img
COPY ./styles.css ./styles.css

CMD python3 -m http.server 8080

