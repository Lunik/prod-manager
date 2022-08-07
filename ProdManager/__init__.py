import os
import logging
from datetime import datetime, timedelta

from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

from ProdManager.helpers.mail import MailWorker
from ProdManager.helpers.lang import LangManager
from ProdManager.helpers.config import boolean_param

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
mail = MailWorker()
lang = LangManager()

def create_app():
  app = Flask(
    __name__,
    instance_relative_config=True,
    static_folder='static',
    static_url_path='/static',
    template_folder='templates'
  )

  app.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY=os.environ.get(
      "PM_SECRET_KEY",
      "changeit"
    ),
    APP_NAME="ProdManager",
    SESSION_COOKIE_NAME=os.environ.get(
      "PM_SESSION_COOKIE_NAME",
      "session_BREAKING_THE_PRODUCTION"
    ),
    SESSION_COOKIE_SAMESITE="Strict",
    # store the database in the instance folder
    SQLALCHEMY_DATABASE_URI=os.environ.get(
      "PM_DATABASE_URI",
      f"sqlite:///{os.path.join(app.instance_path, 'ProManager.sqlite')}"
    ),
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    SQLALCHEMY_ECHO=boolean_param(os.environ.get("PM_SQLALCHEMY_ECHO", 'False')),
    WTF_CSRF_ENABLED=True,
    WTF_CSRF_CHECK_DEFAULT=False,
    CUSTOM_CSS_SHEET=os.environ.get("PM_CUSTOM_CSS_SHEET", None),
    MAIL_ENABLED=boolean_param(os.environ.get("PM_MAIL_ENABLED", 'False')),
    MAIL_SERVER=os.environ.get("PM_MAIL_SERVER", None),
    MAIL_PORT=int(os.environ.get("PM_MAIL_PORT", 587)),
    MAIL_USERNAME=os.environ.get("PM_MAIL_USERNAME", None),
    MAIL_PASSWORD=os.environ.get("PM_MAIL_PASSWORD", None),
    MAIL_USE_SSL=boolean_param(os.environ.get("PM_MAIL_USE_SSL", 'False')),
    MAIL_USE_TLS=boolean_param(os.environ.get("PM_MAIL_USE_TLS", 'True')),
    MAIL_VALIDATE_CERTS=boolean_param(os.environ.get("PM_MAIL_VALIDATE_CERTS", 'True')),
    MAIL_USE_CREDENTIALS=boolean_param(os.environ.get("PM_MAIL_USE_CREDENTIALS", 'True')),
    MAIL_SENDER=os.environ.get("PM_MAIL_SENDER", None),
    MAIL_PREFIX=os.environ.get("PM_MAIL_PREFIX", "[ProdManager] "),
    MAIL_REPLY_TO=os.environ.get("PM_MAIL_REPLY_TO", None),
    LANG=os.environ.get("PM_LANG", "en"),
  )

  app.wsgi_app = ProxyFix(app.wsgi_app, x_for=0, x_proto=1)

  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  csrf.init_app(app)

  from ProdManager.helpers.auth import retreiv_auth
  from ProdManager.helpers.api import retreiv_api
  from ProdManager.helpers.security import validate_csrf
  from ProdManager.helpers.pagination import secure_pagination
  @app.before_request
  def pre_request():
    retreiv_auth()
    retreiv_api()
    validate_csrf()
    secure_pagination()

  from ProdManager.helpers.security import add_security_headers
  @app.after_request
  def pre_response(response):
    response = add_security_headers(response)

    return response

  # register the database commands
  db.init_app(app)
  migrate.init_app(app, db)

  mail.init_app(app)
  lang.init_app(app)

  # apply Gunicorn logger config
  gunicorn_logger = logging.getLogger('gunicorn.error')
  gunicorn_logger.setLevel(gunicorn_logger.level)
  app.logger.handlers = gunicorn_logger.handlers

  from ProdManager.errors import (
    page_not_found, conflict, forbiden,
    internal_error, bad_request,
  )

  app.register_error_handler(400, bad_request)
  app.register_error_handler(403, forbiden)
  app.register_error_handler(404, page_not_found)
  app.register_error_handler(409, conflict)
  app.register_error_handler(500, internal_error)

  from ProdManager.models import (
    Incident, IncidentEvent, Maintenance, MaintenanceEvent,
    Monitor, Subscriber, Scope, Service,
  )


  from ProdManager.routes import (
    root, auth, scope, service, incident,
    maintenance, monitor, health, notification,
  )
  # apply the blueprints to the app
  app.register_blueprint(root.view, url_prefix="/")
  app.register_blueprint(auth.view, url_prefix="/")
  app.register_blueprint(scope.view, url_prefix="/scope")
  app.register_blueprint(scope.view, url_prefix="/api/scope", name="scope_api")
  app.register_blueprint(service.view, url_prefix="/service")
  app.register_blueprint(service.view, url_prefix="/api/service", name="service_api")
  app.register_blueprint(incident.view, url_prefix="/incident")
  app.register_blueprint(incident.view, url_prefix="/api/incident", name="incident_api")
  app.register_blueprint(maintenance.view, url_prefix="/maintenance")
  app.register_blueprint(maintenance.view, url_prefix="/api/maintenance", name="maintenance_api")
  app.register_blueprint(monitor.view, url_prefix="/monitor")
  app.register_blueprint(monitor.view, url_prefix="/api/monitor", name="monitor_api")
  app.register_blueprint(health.view, url_prefix="/health")
  app.register_blueprint(notification.view, url_prefix="/notification")

  from ProdManager.helpers.jinja2 import (
    ternary, format_column_name, format_timeline_date,
    format_template_name,
  )
  from ProdManager.helpers.pagination import url_for_paginated
  from ProdManager.helpers.links import custom_url_for
  from ProdManager.helpers.lang.tools import text

  app.jinja_env.filters['ternary'] = ternary
  app.jinja_env.filters['format_column_name'] = format_column_name
  app.jinja_env.filters['format_timeline_date'] = format_timeline_date
  app.jinja_env.filters['format_template_name'] = format_template_name
  app.jinja_env.globals['url_for_paginated'] = url_for_paginated
  app.jinja_env.globals['custom_url_for'] = custom_url_for
  app.jinja_env.globals['_'] = text


  return app
