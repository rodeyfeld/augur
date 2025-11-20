FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
  UV_PROJECT_ENV=.venv \
  PATH="/app/.venv/bin:${PATH}"

WORKDIR /app

RUN apt-get update \
  && apt-get install -y \
  curl \
  vim \
  gdal-bin \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
  && mv /root/.local/bin/uv /usr/local/bin/uv \
  && mv /root/.local/bin/uvx /usr/local/bin/uvx


FROM base AS builder
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . .
RUN uv sync --frozen --no-dev
RUN python manage.py collectstatic --noinput


FROM base AS dev
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY . .
CMD ["bash", "-c", "uv sync --frozen --no-dev && uv run manage.py runserver 0.0.0.0:8000"]


FROM base AS prod
COPY --from=builder /app /app
RUN useradd -ms /bin/bash augur && chown -R augur:augur /app
USER augur
CMD ["gunicorn", "--bind=0.0.0.0:8000", "--capture-output", "--log-level=info", "--access-logfile=-", "--error-logfile=-", "--timeout=60", "--forwarded-allow-ips=*", "augur.wsgi:application"]
