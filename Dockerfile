FROM python:3.11-rc-bullseye

RUN mkdir /workdir

WORKDIR /workdir

RUN apt-get update && apt-get install -y jq

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
