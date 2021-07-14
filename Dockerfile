FROM python:3.9-alpine

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
	gcc libc-dev linux-headers postgresql-dev 
RUN apk add --update --no-cache zlib libjpeg
RUN apk add build-base python3-dev py-pip jpeg-dev zlib-dev
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt
RUN apk del .tmp-build-deps


RUN mkdir /backend
WORKDIR /backend
COPY ./ /backend