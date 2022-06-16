FROM python:3-alpine

WORKDIR /app
ENV PYTHONPATH=/app

RUN apk add \
  --update --no-cache \
  make


ADD requirements.txt Makefile ./
RUN apk add --update --no-cache --virtual .build build-base \
  && make install-docker \
  && apk del .build

ADD ProdManager ProdManager
ADD migrations migrations
ADD main.py .flaskenv ./

RUN python -m compileall ProdManager main.py

ENV GUNICORN=/usr/local/bin/gunicorn
ENV FLASK=/usr/local/bin/flask
ENV SERVER=0.0.0.0
ENV PORT=8080

CMD ["make", "run"]