FROM python:3-alpine3.7

# Making my life suck
LABEL Maintianer="Anish Gupta"

# Exposing endpoint port
EXPOSE 8888

# Setting mode directory
RUN mkdir -p /home/app
COPY . /home/app
WORKDIR /home/app

# Installing utils and deps
RUN apk install g++
RUN pip3 install -r -U requirements.txt

ENTRYPOINT [ "python3", "main.py" ]