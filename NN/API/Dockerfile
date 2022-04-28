# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-deps -r requirements.txt

RUN apt-get update && apt-get -y install ffmpeg libsndfile1-dev

COPY . .

CMD export FLASK_APP=main && flask run --host=0.0.0.0
