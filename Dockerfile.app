FROM python:3.8-alpine
LABEL maintainer="Alexey Romanov"

ENV PYTHONBUFFERED 1

RUN apk add --update --no-cache postgresql-client libxslt-dev libxml2-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc postgresql-dev musl-dev

COPY ./requirements.txt /requirements.txt
RUN python3 -m pip install -r /requirements.txt

RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app

RUN adduser -D admin
USER admin
