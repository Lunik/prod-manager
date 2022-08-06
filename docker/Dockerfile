FROM python:3-alpine

WORKDIR /app
ENV PYTHONPATH=/app

RUN apk upgrade \
  --update --no-cache \
  && apk add \
  --update --no-cache \
  make ca-certificates


COPY Makefile ./
RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
  apk add --update --no-cache --virtual .build build-base \
  && make install-docker \
  && apk del .build

COPY ProdManager ProdManager
COPY migrations migrations
COPY main.py .flaskenv ./

RUN python -m compileall ProdManager main.py

ENV GUNICORN=/usr/local/bin/gunicorn
ENV FLASK=/usr/local/bin/flask
ENV SERVER=0.0.0.0

ARG PORT=8080
ENV PORT=$PORT
EXPOSE $PORT

CMD ["make", "run"]