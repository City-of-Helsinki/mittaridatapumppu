## Introduction

This repository contains a development environment for the Mittaridatapumppu project.

It is based on the microservices architecture and consists of the following services:
- [deviceregistry](https://github.com/City-of-Helsinki/mittaridatapumppu)
- [endpoint](https://github.com/City-of-Helsinki/mittaridatapumppu-endpoint)
- [parser](https://github.com/City-of-Helsinki/mittaridatapumppu-parser)
- [persister](https://github.com/City-of-Helsinki/mittaridatapumppu-persister)

Local Kafka is used as a message broker between the services.
For demo purposes there is also an InfluxDB V2 database for storing the parsed data.

Included [docker-compose.yml](docker-compose.yml) file is for running
the whole pipeline locally.

There are also some scripts for populating the database with real data.

## Developer's guide

### Clone the repo
```shell
git clone --recurse-submodules git@github.com:City-of-Helsinki/mittaridatapumppu.git
```

### Branches

Create applicable branches in sub-repositories where needed while developing,
e.g. `feature/new-feature` or `bugfix/bugfix-description`.

### Developing with Docker

Set up the environment by building the images and loading initial data for development.

```shell
docker compose up --build
docker compose exec deviceregistry python manage.py loaddata devices/fixtures/auth.json devices/fixtures/authtoken.json devices/fixtures/endpoints.json
```

Later on you can start the services with

```shell
docker compose up
```

#### Developing without Docker

<strike>
Do not use this for now. It is not tested with the latest code and probably does not work.

```shell
dropdb deviceregistry
createdb deviceregistry
psql deviceregistry -c "create extension postgis;commit;"
export DEBUG=1
export DATABASE_LOCAL=1
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata devices/fixtures/auth.json devices/fixtures/authtoken.json devices/fixtures/endpoints.json
```
</strike>

### Log in to Django admin

Go to http://localhost:8000/admin/ and login with `root` and `ruutruut`. Check
that there are some
[endpoints](http://127.0.0.1:8000/admin/endpoints/endpoint/) defined.

Verify that the [hosts endpoint](http://127.0.0.1:8000/api/v1/hosts/localhost/)
returns localhost and at least 2 endpoints.

### Populate database with real data

You will need to have the device registry service (deviceregistry) running and
an Excel file containing data of devices and locations and uirasmeta.py,
which contains additional metadata of UiRaS sensors.

```shell
python mittaridatapumppu/devices/scripts/populate_db_via_api.py --api-url http://127.0.0.1:8000/api/v1/ --api-token abcdef1234567890abcdef1234567890abcdef12 --excel-file Mittaridatapumppu-initial-data.xlsx
python mittaridatapumppu/devices/scripts/populate_db_via_api.py --api-url http://127.0.0.1:8000/api/v1/ --api-token abcdef1234567890abcdef1234567890abcdef12 --uirasmeta

# Try it out with httpie (https://httpie.org/):
http GET http://127.0.0.1:8000/api/v1/devices/70B3D57050011422/ "Authorization:Token abcdef1234567890abcdef1234567890abcdef12"
# The same with curl:
curl http://127.0.0.1:8000/api/v1/devices/70B3D57050011422/ -H "Authorization:Token abcdef1234567890abcdef1234567890abcdef12" | jq
```

### Send data to the pipeline

```shell
python mittaridatapumppu-endpoint/tests/test_api2.py
```

Check docker logs what happens.

### Check the data in InfluxDB

Go to http://localhost:18086/ and login with `root` and `ruutruut`.

### Check the data in Django admin

Go to http://localhost:8000/admin/ and login with `root` and `ruutruut`.

### Running the tests

Currently, there are both Django tests and pytest tests.

Run tests:

```shell
docker compose exec deviceregistry python manage.py test devices/tests
docker compose exec deviceregistry pytest devices/tests/test_api_devicetype.py
docker compose exec deviceregistry pytest devices/tests/test_api_device.py
```

Later only pytest tests will be used.

## Code Formatting

## Linting

## Pre-commit hook
