FROM python:3.8

RUN mkdir /app
WORKDIR /app

# Copy over the files
COPY ./frontend ./frontend/
COPY ./backend ./backend/
COPY ./flag.txt ./flag.txt 
COPY ./run.sh ./run.sh 

# Set up dependencies
RUN pip3 install -r ./backend/requirements.txt


#CMD sleep 10000000
CMD ./run.sh 


