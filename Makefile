PY       ?= python3
DOCKER   ?= docker
KUBECTL  ?= kubectl
VENV_PY  ?= venv/bin/python3
FLASK    ?= venv/bin/flask
GUNICORN ?= venv/bin/gunicorn
PYLINT   ?= venv/bin/pylint
PYTEST   ?= venv/bin/pytest

VENV             ?= venv
REQUIREMENTS      = requirements.txt
REQUIREMENTS_DEV  = requirements.dev.txt

APP_NAME = prod-manager
PACKAGE_NAME = ProdManager

SERVER    ?= 127.0.0.1
PORT      ?= 8080
WORKERS   ?= 2
THREADS   ?= 2

FLASK_OPTS = --host="${SERVER}" --port="${PORT}"
GUNICORN_OPTS = --bind="${SERVER}:${PORT}" --workers=${WORKERS} --threads=${THREADS}

DOCKER_COMPOSE_OPTS = --project-directory="deploy/compose" --project-name="${APP_NAME}"
KUBECTL_OPTS = --filename="deploy/kubernetes"

SONAR_BRANCH = $(shell git rev-parse --abbrev-ref HEAD)

STATICS = ProdManager/static

APP_VERSION = $(shell git rev-parse HEAD)

help:
	@echo 'Makefile for a ProdManager                                                '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make env			Setup Python virtual env                                 '
	@echo '   make install	Install required packages                                '
	@echo '   make rundev		Start application in developpement mode                  '
	@echo '   make run			Start application in production mode                     '
	@echo '                                                                          '
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html   '
	@echo '                                                                          '

install: env
	${VENV_PY} -m pip install -r "${REQUIREMENTS}"

install-dev: env
	${VENV_PY} -m pip install -r "${REQUIREMENTS_DEV}"

install-docker:
	${PY} -m pip install --compile -r "${REQUIREMENTS}"

env:
	${PY} -m venv "${VENV}"


run-dev:
	${GUNICORN} ${GUNICORN_OPTS} --reload --log-level="debug" "main:app"


run-kube: build-docker
	${KUBECTL} apply ${KUBECTL_OPTS}

stop-kube:
	${KUBECTL} delete ${KUBECTL_OPTS}


run-docker: build-docker
	${DOCKER} compose ${DOCKER_COMPOSE_OPTS} up --detach

stop-docker:
	${DOCKER} compose ${DOCKER_COMPOSE_OPTS} down --remove-orphans --volumes

build-docker:
	${DOCKER} build --file="docker/Dockerfile" --tag="${APP_NAME}:$(APP_VERSION)" .


run:
	${GUNICORN} ${GUNICORN_OPTS} "main:app"

database-upgrade:
	${FLASK} db upgrade

sonar: lint test
	sonar-scanner \
	  -Dsonar.branch.name="$(SONAR_BRANCH)"

check: lint

lint:
	${PYLINT} ${PACKAGE_NAME}/* tests/${PACKAGE_NAME}/* | tee pylint-report.txt

test:
	${PYTEST} --cov --cov-report xml:coverage.xml --junitxml=result.xml ${PACKAGE_NAME}/ tests/${PACKAGE_NAME}/