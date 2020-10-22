
FROM python:3.8.2-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /app && \
    apt-get update
RUN apt-get install build-essential python -y
WORKDIR /app
RUN pip install pip-tools
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

CMD celery worker -A ticketmaster --loglevel=info

CMD uwsgi --http 0.0.0.0:8000 --wsgi-file ticketmaster/ticketmaster/wsgi.py



