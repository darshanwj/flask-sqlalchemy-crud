FROM python:3.9-slim-buster

RUN apt update && apt install -y  \
    gcc \
    default-libmysqlclient-dev