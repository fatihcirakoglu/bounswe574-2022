# Alpine base image that contains python 3.8.2
FROM python:3.8.2-alpine

MAINTAINER Fatih Cirakoglu "fatih.cirakoglu@boun.edu.tr"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY . /app
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN apk --no-cache add curl \
  && pip install --no-cache-dir -r requirements.txt \
  && pip install -e . \
  && rm -rf /var/cache/apk/*

EXPOSE 5000

# CMD python ./run.py
