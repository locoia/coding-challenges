FROM python:3.9-slim-buster

RUN mkdir -p /usr/src/locoia
WORKDIR /usr/src/locoia
COPY ./ /usr/src/locoia

RUN pip install --no-cache-dir -r requirements.txt
