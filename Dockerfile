# pull official base image
FROM python:3.9.6-alpine as builder

ENV PYTHONUNBUFFERED=1
ENV TZ="Europe/Moscow"

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /code/
