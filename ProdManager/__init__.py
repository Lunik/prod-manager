import os
import logging
from datetime import datetime, timedelta

from flask import Flask, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

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
    # store the database in the instance folder
    SQLALCHEMY_DATABASE_URI=os.environ.get(
      "PM_DATABASE_URI",
      f"sqlite:///{os.path.join(app.instance_path, 'ProManager.sqlite')}"
    ),
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    SQLALCHEMY_ECHO=False,
    WTF_CSRF_ENABLED=True
  )

  app.config.from_pyfile("config.py", silent=True)

  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  csrf.init_app(app)

  # register the database commands
  db.init_app(app)
  migrate.init_app(app, db)

  # apply Gunicorn logger config
  gunicorn_logger = logging.getLogger('gunicorn.error')
  gunicorn_logger.setLevel(gunicorn_logger.level)
  app.logger.handlers = gunicorn_logger.handlers

  # from ProdManager.errors import error_404

  # app.register_error_handler(404, error_404)


  from ProdManager.helpers.auth import retreiv_auth
  @app.before_request
  def load_logged():
    retreiv_auth()


  from ProdManager.routes import root,auth,scope,service,incident,maintenance,monitor
  # apply the blueprints to the app
  app.register_blueprint(root.view, url_prefix="/")
  app.register_blueprint(auth.view, url_prefix="/")
  app.register_blueprint(scope.view, url_prefix="/scope")
  app.register_blueprint(service.view, url_prefix="/service")
  app.register_blueprint(incident.view, url_prefix="/incident")
  app.register_blueprint(maintenance.view, url_prefix="/maintenance")
  app.register_blueprint(monitor.view, url_prefix="/monitor")

  from ProdManager.filters.basic import (
    ternary, format_column_name, format_timeline_date,
    format_template_name,
  )

  app.jinja_env.filters['ternary'] = ternary
  app.jinja_env.filters['format_column_name'] = format_column_name
  app.jinja_env.filters['format_timeline_date'] = format_timeline_date
  app.jinja_env.filters['format_template_name'] = format_template_name


  return app
