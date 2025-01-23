FROM python:3.10-slim

WORKDIR /app
RUN pip install poetry
COPY . .
RUN poetry install

ENV PYTHONPATH=/app/src
