# pull official base image
FROM python:3.11.3-slim

# create directory for the app user
RUN mkdir -p /project

# create the app user
RUN addgroup --system app && adduser --system --group app

ENV APP_HOME=/home/app
WORKDIR $APP_HOME

# copy project
COPY . $APP_HOME

# install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

#give permission to store media
RUN chown -R app:app /media

# change to the app user
USER app

ENV DJANGO_SETTINGS_MODULE=deviceregistry.settings
# start django server
CMD python manage.py runserver 0.0.0.0:8000
