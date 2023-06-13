System Test


# Prerequisites

docker,
docker-compose

# Development

## Virtualenv

Create a virtualenv for test scripts and install the requirements
```
python3.11 -m venv venv-test
source venv-test/bin/activate
pip install -r requirements.txt
```


# How to Set up and Test the system works


## set up services

```
docker-compose up --build -d
```


###  Get deviceregstry up and functional

```
docker-compose exec devreg python manage.py migrate
docker-compose exec devreg python manage.py createsuperuser
<Configure user to your satisfaction>
<Verify that you can login at 127.0.0.1:8000/admin/ >
```
#### to run device registry tests:
```
          docker-compose exec devreg python manage.py test devices/tests
          docker-compose exec devreg pytest devices/tests/test_api_device.py
          docker-compose exec devreg pytest devices/tests/test_api_devicetype.py
```
### Access Tokens

Go to http://127.0.0.1:8000/admin/authtoken/tokenproxy/
and create a new token for your user.
Then you can use the token to access the API, e.g.

```
http -v GET http://127.0.0.1:8000/api/v1/users/ "Authorization: Token abcs1234bacbbacb12431232123"
```

### Verify endpoint service is up

access the web interface at http://127.0.0.1:8001/digita/v2

If it works, you should see a message `Missing or invalid authentication token`.

run script thats send post request with auth token (test token) and verify a  'HTTP/1.1 202 Accepted' response

```
sh 70B3D50123456789.sh
```
#### to run endpoint tests:
```
docker-compose exec endpoint-digita python -m pytest tests/test_api.py
```
### Populate Database

### Update device registry access token to parser service

### verify post call to endpoint goes through other services
