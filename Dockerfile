# syntax=docker/dockerfile:1

FROM python:3.11-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.11-slim

ARG VERSION=dev
LABEL org.opencontainers.image.title="med-control" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.source="https://github.com/VictorHugoDantas/med-control"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    APP_VERSION=${VERSION}

COPY --from=builder /install /usr/local

RUN useradd --create-home --uid 1000 medcontrol \
    && mkdir -p /data \
    && chown medcontrol:medcontrol /data

WORKDIR /app
COPY src/ ./src/
COPY VERSION .

USER medcontrol
WORKDIR /data
VOLUME ["/data"]

CMD ["python", "/app/src/main.py"]
