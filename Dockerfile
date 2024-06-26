# mittaridatapumppu-deviceregistry

FROM python:3.11-alpine

LABEL org.opencontainers.image.source=https://github.com/city-of-helsinki/mittaridatapumppu
LABEL org.opencontainers.image.description="Mittaridatapumppu Device Registry"
LABEL org.opencontainers.image.licenses="Apache License 2.0"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Override these in the docker-compose.yml file or elsewhere

# PostgreSQL config
ENV DJANGO_DB_NAME=postgres
ENV DJANGO_DB_USER=postgres
ENV DJANGO_DB_PASSWORD=postgres
ENV DJANGO_DB_HOST=db
ENV DJANGO_DB_PORT=5432

# Device registry config
ENV DJANGO_SETTINGS_MODULE=deviceregistry.settings
ENV MEDIA_ROOT=/media
ENV STATIC_ROOT=/static

COPY entrypoint.sh /

# Install GeoDjango dependencies and binutils to help Django find them
RUN apk add --no-cache \
  geos-dev \
  proj-dev \
  gdal-dev \
  binutils

RUN addgroup -S app && adduser -S app -G app
WORKDIR /home/app

# Copy and install requirements only first to cache the dependency layer
COPY --chown=app:app requirements.txt .
RUN pip install --no-cache-dir --no-compile --upgrade -r requirements.txt

COPY --chown=app:app . .

# Support Arbitrary User IDs
RUN chgrp -R 0 /home/app && \
  chmod -R g+rwX /home/app

RUN python manage.py collectstatic --noinput

USER app

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "deviceregistry.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--lifespan", "off"]
EXPOSE 8000/tcp
