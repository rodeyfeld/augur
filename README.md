# Augur

Django REST API for satellite imagery search and geospatial analysis.

Docs at http://127.0.0.1:8000/api/docs locally

## Running locally

```bash
cp example.env .env
```

## Docker

Dev:

```bash
docker compose up
```

Prod:

```bash
docker build --tag edrodefeld/augur .
docker push edrodefeld/augur:latest
```
