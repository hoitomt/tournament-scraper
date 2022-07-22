FROM python:3.11-rc-bullseye

RUN mkdir /workdir

WORKDIR /workdir

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y jq

RUN pip install -r requirements.txt