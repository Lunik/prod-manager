PY       ?= python3
DOCKER   ?= docker
KUBECTL  ?= kubectl
VENV_PY  ?= venv/bin/python3
FLASK    ?= venv/bin/flask
GUNICORN ?= venv/bin/gunicorn
PYLINT   ?= venv/bin/pylint
PYTEST   ?= venv/bin/pytest
COVERAGE ?= venv/bin/coverage

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

GIT_BRANCH = $(shell git rev-parse --abbrev-ref HEAD)

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
	${PY} -m pip install --no-cache-dir --compile -r "${REQUIREMENTS}"

env:
	${PY} -m venv "${VENV}"


run-dev:
	${GUNICORN} ${GUNICORN_OPTS} --reload --log-level="debug" "main:app"


run-kube: build-docker
	${KUBECTL} apply ${KUBECTL_OPTS}

stop-kube:
	${KUBECTL} delete ${KUBECTL_OPTS}


run-docker:
	${DOCKER} compose ${DOCKER_COMPOSE_OPTS} up --detach

stop-docker:
	${DOCKER} compose ${DOCKER_COMPOSE_OPTS} down --remove-orphans --volumes

build-docker:
	${DOCKER} build --file="docker/Dockerfile" --tag="${APP_NAME}:$(APP_VERSION)" .


run: $(if $(PM_STANDALONE), database-upgrade) $(if $(PM_DEMO), demo-data)
	${GUNICORN} ${GUNICORN_OPTS} "main:app"

demo-data-dev: database-upgrade
	PYTHONPATH=. $(VENV_PY) ProdManager/demo/init.py

demo-data: database-upgrade
	PYTHONPATH=. python3 ProdManager/demo/init.py

database-migration:
	${FLASK} db migrate -m "<EDIT COMMIT MESSAGE>"

database-upgrade:
	${FLASK} db upgrade

check: lint

lint:
	${PYLINT} ${PACKAGE_NAME}/* | tee pylint-report.txt

test:
	${VENV_PY} -m pytest -v -n 4 --cov=${PACKAGE_NAME} --junitxml=result.xml --html=report.html tests/${PACKAGE_NAME}/ \
	&& ${COVERAGE} xml \
	&& ${COVERAGE} html

show-test: show-tests show-coverage

show-tests:
	open report.html

show-coverage:
	open htmlcov/index.html
