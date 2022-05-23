# Alpine base image that contains python 3.8.2
FROM python:3.8.2-alpine

MAINTAINER Fatih Cirakoglu "fatih.cirakoglu@boun.edu.tr"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./src /app
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN apk update && apk add --update py-pip && apk add --no-cache \
    mysql mysql-dev gcc python3-dev musl-dev libffi-dev python-dev jpeg-dev\ 
    && pip install --no-cache-dir -r requirements.txt
