FROM python:3.10.7-alpine AS base

WORKDIR /usr/src/votala

ENV PYTHONDONTWRITEBYTECODE=1

COPY deps/* /usr/src/votala/

# :)
RUN pip install --upgrade pip

# Install the requirements for fastapi and another rest utilitites
RUN pip install -r  rest_requirements.txt

# Install the requirements for database communication
RUN pip install -r  database_requirements.txt

# Install the requirements for message broker(RabbitMQ)
RUN pip install -r  message_broker_requirements.txt

# Install the requirements for another dependencies
RUN pip install -r  extra_requirements.txt


