FROM python:3.10.7-alpine AS base

WORKDIR /usr/src/email_handler
COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir
