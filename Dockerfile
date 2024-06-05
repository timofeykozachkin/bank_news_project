FROM python:3.11-slim

WORKDIR /app
ADD ./requirements.txt /app/requirements.txt

RUN pip3 install -U pip
RUN pip3 install -r requirements.txt

COPY . /app

CMD gunicorn -b 0.0.0.0:80 app:server
