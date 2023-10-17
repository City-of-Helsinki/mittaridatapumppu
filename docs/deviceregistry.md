Django App for Device Registry

docker development environment with django and postgres

# Prerequisites

docker,
docker-compose

# Development

## Virtualenv

Create a virtualenv for the project and install the requirements, e.g.

```
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pip install -r requirements.txt
```

## pre-commit hooks

Install pre-commit hooks to your virtualenv

```
pre-commit install
```



# Setting up

```
docker-compose up --build -d
docker-compose exec deviceregistry python manage.py migrate
docker-compose exec deviceregistry python manage.py createsuperuser
<Configure user to your satisfaction>
<Verify that you can login at 127.0.0.1:8000/admin/ >
```

# Running Tests

for api tests:
```
docker-compose exec deviceregistry pytest devices/tests/test_api.py
```

for model and admin page tests

```
docker-compose exec deviceregistry python manage.py test devices/tests
```

# Misc stuff

## PostgreSQL connection

To open psql shell in the db container:

```
docker-compose exec db psql -U postgres
```

## API connection

Go to http://127.0.0.1:8000/admin/authtoken/tokenproxy/
and create a new token for your user.
Then you can use the token to access the API, e.g.

```
http -v GET http://127.0.0.1:8000/api/v1/users/ "Authorization: Token abcs1234bacbbacb12431232123"
```
