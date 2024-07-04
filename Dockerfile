FROM python:3.10-slim as bqp-api-server

ENV TZ="Europe/Berlin"

ARG PYTHONUNBUFFERED
ARG QUANTUM_DB_USER
ARG QUANTUM_DB_PASS
ARG QUANTUM_DB_HOST

RUN apt update && apt install -y git

RUN mkdir -p /bqp-api-server
COPY gunicorn.conf.py /bqp-api-server/
COPY pyproject.bqp-api.toml /bqp-api-server/pyproject.toml
WORKDIR /bqp-api-server

RUN pip install pdm
RUN pdm install
ENV PYTHONPATH=.

EXPOSE 4000

# Run the server
ENTRYPOINT [".venv/bin/gunicorn", "-c","gunicorn.conf.py"]