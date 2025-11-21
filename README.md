# Augur

Django REST API for satellite imagery search and geospatial analysis.

Docs at http://127.0.0.1:8000/api/docs locally or https://augur.pinwheel.fan/api/docs in prod.

## Running locally

Make a `.env` file:
```bash
AUGUR_DEBUG=True
AUGUR_SECRET_KEY=my-secret
AUGUR_ALLOWED_HOSTS=localhost,127.0.0.1
AUGUR_SESSION_COOKIE_SECURE=False
AUGUR_CSRF_COOKIE_SECURE=False
AUGUR_SECURE_SSL_REDIRECT=False
AUGUR_DB_NAME=augur
AUGUR_DB_USER=postgres
AUGUR_DB_PASSWORD=postgres
AUGUR_DB_HOST=localhost
AUGUR_DB_PORT=5432
```

Then:
```bash
python manage.py migrate
python manage.py runserver
```

## Docker

Dev:
```bash
docker build --tag augur .
docker run -p 8000:8000 --name augur augur
```

Prod:
```bash
docker build --tag edrodefeld/augur .
docker push edrodefeld/augur:latest
```

## Deploy to k8s

```bash
kubectl apply -f ../mirage/deployments/augur.yml
kubectl rollout restart deployment/augur -n galaxy
```
