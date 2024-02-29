FROM python:3.10-slim as bqp-api-server

ENV TZ="Europe/Berlin"

ARG PYTHONUNBUFFERED
ARG QUANTUM_DB_USER
ARG QUANTUM_DB_PASS
ARG QUANTUM_DB_HOST

RUN apt update && apt install -y git

RUN mkdir -p /bqp-api
COPY * /bqp-api/
WORKDIR /bqp-api

RUN pip install pdm
RUN pdm install
RUN pdm update
ENV PYTHONPATH=.

# Run the server
ENTRYPOINT [".venv/bin/gunicorn", "-c","gunicorn.conf.py"]