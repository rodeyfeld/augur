FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /augur
RUN apt-get update \
  && apt-get install -y \
  vim \
  gdal-bin \
  && apt-get clean

RUN useradd -ms /bin/bash augur
COPY . /augur
RUN pip install --upgrade pip pip-tools
RUN pip-compile --output-file=requirements.txt pyproject.toml
RUN pip-sync
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
RUN python manage.py collectstatic

CMD ["gunicorn", "--bind=0.0.0.0:8000", "--capture-output", "--log-level=debug", "--access-logfile=-", "--error-logfile=-", "--timeout=60", "--forwarded-allow-ips=*", "augur.wsgi:application"]
