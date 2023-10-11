# mittaridatapumppu-deviceregistry

FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Override these in the docker-compose.yml file or elsewhere
ENV DATABASE_NAME=postgres
ENV DATABASE_USER=postgres
ENV DATABASE_PASSWORD=postgres
ENV DATABASE_HOST=db
ENV DATABASE_PORT=5432

ENV MEDIA_HOME=/media
ENV DJANGO_SETTINGS_MODULE=deviceregistry.settings

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

USER app

# start django server
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]
