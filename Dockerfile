FROM python:3.6.5

# Making my life suck
LABEL Maintianer="Anish Gupta"

# Exposing endpoint port
EXPOSE 8888

# Setting mode directory
RUN mkdir -p /home/app
COPY . /home/app
WORKDIR /home/app
ENTRYPOINT [ "pipenv", "run", "python", "main.py" ]

# Installing utils and deps
RUN apt-get update \
    && apt-get install -y gcc git python-dev \
    && apt-get clean

RUN pip install pipenv

RUN pipenv install
