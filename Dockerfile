FROM python:3.12.1-slim-bullseye AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    musl-dev

COPY requirements.txt /app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY /app/ /app/**
