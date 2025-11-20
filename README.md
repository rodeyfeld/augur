# AUGUR
Django Ninja REST API for effectively managing access to the Dreamflow project.

Docs are auto generated and hosted at 
- http://127.0.0.1:8000/api/docs



## local setup
Create a `.env` file
```
# Django
AUGUR_DEBUG=True
AUGUR_SECRET_KEY=my-secret
AUGUR_ALLOWED_HOSTS=localhost,127.0.0.1
AUGUR_SESSION_COOKIE_SECURE=False
AUGUR_CSRF_COOKIE_SECURE=False
AUGUR_SECURE_SSL_REDIRECT=False
# Postgres
AUGUR_DB_NAME=augur
AUGUR_DB_USER=postgres
AUGUR_DB_PASSWORD=postgres
AUGUR_DB_HOST=localhost
AUGUR_DB_PORT=5432
```

Run the commands found in the base README.md to activate virtualenvironment.

```
python manage.py migrate
python manage.py runserver
```

## docker
```
docker build --tag augur .
docker run -p 8000:8000 --name augur --network=pythosnet augur
```

## docker (prod)
```
echo .env >> .dockerignore
docker build --tag edrodefeld/augur .
docker push edrodefeld/augur:latest
```

## run server via gunicorn
```
gunicorn  --bind 0.0.0.0:8000 --workers 2 augur.wsgi
```
