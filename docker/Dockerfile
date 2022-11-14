FROM python:3-alpine

# Dockerfile arguments
ARG APP_DIR=/app
ARG FLASK_INSTANCE_DIR=$APP_DIR/instance
ARG USER=prodmanager
ARG PORT=8080


# Define base configuration
ENV PYTHONPATH=$APP_DIR
ENV GUNICORN=/usr/local/bin/gunicorn
ENV FLASK=/usr/local/bin/flask
ENV SERVER=0.0.0.0
ENV PORT=$PORT


# Change base directory
WORKDIR $APP_DIR


# Create application user & work directory
RUN adduser \
    -u 1000 \
    -D -H \
    -h $APP_DIR \
    $USER \
  && mkdir $FLASK_INSTANCE_DIR \
  && chown $USER:$USER $FLASK_INSTANCE_DIR


# Upgrade base image
RUN apk upgrade \
  --update --no-cache \
  && apk add \
  --update --no-cache \
  make ca-certificates


# Install required libraries/packages
COPY Makefile ./
RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
  apk add --update --no-cache --virtual .build build-base \
    libxml2-dev libxslt-dev postgresql-dev \
  && make install-docker \
  && apk del .build


# Copy application sources
COPY ProdManager ProdManager
COPY migrations migrations
COPY main.py .flaskenv ./


# Compile app Python files
RUN python -m compileall ProdManager main.py


# Change user for runtime
USER $USER

# Declare application data volume
VOLUME $FLASK_INSTANCE_DIR

# Declare application listen port
EXPOSE $PORT

# Declare application command start
CMD ["make", "run"]