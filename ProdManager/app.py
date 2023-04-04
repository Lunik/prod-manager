import os
import logging
from datetime import timedelta

from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask

from ProdManager.helpers.config import boolean_param
from ProdManager.helpers.version import AppVersion
from ProdManager.helpers.hello import Hello
from .plugins import (
  db, migrate, csrf, mail, lang, redis_client, markdown, oidc,
  scheduler
)

__version__ = "v0.21.1"
GIT_PROJECT_URL = "https://gitlab.com/prod-manager/prod-manager"
GIT_PROJECT_ID = 36953895
LATEST_VERSION_URL = f"https://gitlab.com/api/v4/projects/{GIT_PROJECT_ID}/releases/permalink/latest"

def create_app(scheduled_jobs=True):
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
    PERMANENT_SESSION_LIFETIME=timedelta(days=7),
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
    MAIL_PREFIX=os.environ.get("PM_MAIL_PREFIX", "[ProdManager]"),
    MAIL_REPLY_TO=os.environ.get("PM_MAIL_REPLY_TO", None),
    LANG=os.environ.get("PM_LANG", "en"),
    DEBUG=boolean_param(os.environ.get("PM_DEBUG", 'False')),
    JWT_ALGORITHM=os.environ.get("PM_JWT_ALGORITHM", "HS256"),
    JWT_ISSUER=os.environ.get("PM_JWT_ISSUER", "ProdManager"),
    API_RATELIMIT_ENABLED=boolean_param(os.environ.get("PM_API_RATELIMIT_ENABLED", 'False')),
    API_RATELIMIT_DEFAULT=int(os.environ.get("PM_API_RATELIMIT_DEFAULT", 60)),
    API_RATELIMIT_LOGGED=int(os.environ.get("PM_API_RATELIMIT_LOGGED", 1500)),
    API_RATELIMIT_PERIOD_HOURS=int(os.environ.get("PM_API_RATELIMIT_PERIOD_HOURS", 1)),
    REDIS_URL=os.environ.get(
      "PM_REDIS_URI",
      "redis://localhost",
    ),
    STATS_ENABLED=boolean_param(os.environ.get("PM_STATS_ENABLED", 'False')),
    OPENID_ENABLED=boolean_param(os.environ.get("PM_OPENID_ENABLED", 'False')),
    OPENID_DISCOVER_URL=os.environ.get("PM_OPENID_DISCOVER_URL", None),
    OPENID_CLIENT_ID=os.environ.get("PM_OPENID_CLIENT_ID", None),
    OPENID_CLIENT_SECRET=os.environ.get("PM_OPENID_CLIENT_SECRET", None),
    OPENID_CLIENT_SCOPES=os.environ.get("PM_OPENID_CLIENT_SCOPES", "openid email profile"),
    OPENID_ROLES_ATTRIBUTE=os.environ.get("PM_OPENID_ROLES_ATTRIBUTE", "roles"),
    OPENID_ALLOWED_ROLE=os.environ.get("PM_OPENID_ALLOWED_ROLE", "admin"),
    DISABLE_VERSION_CHECK=boolean_param(os.environ.get("PM_DISABLE_VERSION_CHECK", 'False')),
    DISABLE_HELLO=boolean_param(os.environ.get("PM_DISABLE_HELLO", 'False')),
  )

  app.scheduler = scheduler
  if scheduled_jobs and not app.scheduler.running:
    app.scheduler.start()

  app.version = AppVersion(
    __version__,
    LATEST_VERSION_URL,
    disable_check=app.config['DISABLE_VERSION_CHECK']
  )

  app.wsgi_app = ProxyFix(app.wsgi_app, x_for=int(os.environ.get("PM_PROXY_CHAIN_COUNT", 1)), x_proto=1)
  if boolean_param(os.environ.get("PM_PROFILING", 'False')):
    from werkzeug.middleware.profiler import ProfilerMiddleware

    os.makedirs('debug', exist_ok=True)
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, sort_by=['cumtime'], profile_dir='debug')

  # ensure the instance folder exists
  os.makedirs(app.instance_path, exist_ok=True)

  csrf.init_app(app)

  from ProdManager.helpers.auth import retreiv_auth
  from ProdManager.helpers.api import retreiv_api, validate_ratelimit_api
  from ProdManager.helpers.security import validate_csrf
  from ProdManager.helpers.pagination import secure_pagination
  @app.before_request
  def pre_request():
    retreiv_api()
    retreiv_auth()
    validate_ratelimit_api()
    validate_csrf()
    secure_pagination()

  from ProdManager.helpers.security import add_security_headers
  from ProdManager.helpers.api import add_ratelimit_api_headers
  @app.after_request
  def pre_response(response):
    response = add_security_headers(response)
    response = add_ratelimit_api_headers(response)

    return response

  # register the database commands
  db.init_app(app)
  migrate.init_app(app, db)

  redis_client.init_app(app)

  mail.init_app(app)
  lang.init_app(app)
  markdown.init_app(app)

  # apply Gunicorn logger config
  gunicorn_logger = logging.getLogger('gunicorn.error')
  gunicorn_logger.setLevel(gunicorn_logger.level)
  app.logger.handlers = gunicorn_logger.handlers

  from ProdManager.errors import (
    page_not_found, conflict, forbiden,
    internal_error, bad_request, unauthorized,
    too_many_requests
  )

  app.register_error_handler(400, bad_request)
  app.register_error_handler(401, unauthorized)
  app.register_error_handler(403, forbiden)
  app.register_error_handler(404, page_not_found)
  app.register_error_handler(409, conflict)
  app.register_error_handler(429, too_many_requests)
  app.register_error_handler(500, internal_error)

  from ProdManager.models import (
    Incident, IncidentEvent, Maintenance, MaintenanceEvent,
    Monitor, Subscriber, Scope, Service, Announcement, AppConfig
  )


  from ProdManager.routes import (
    root, auth, scope, service, incident,
    maintenance, monitor, health, notification,
    weather, token, announcement
  )
  # apply the blueprints to the app
  app.register_blueprint(root.view, url_prefix="/")
  app.register_blueprint(auth.view, url_prefix="/")
  app.register_blueprint(token.view, url_prefix="/api/token", name="token_api")
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
  app.register_blueprint(weather.view, url_prefix="/api/weather", name="weather_api")
  app.register_blueprint(announcement.view, url_prefix="/announcement")
  app.register_blueprint(announcement.view, url_prefix="/api/announcement", name="announcement_api")

  if app.config.get('OPENID_ENABLED'):
    oidc.init_app(app)
    from ProdManager.routes import openid
    app.register_blueprint(openid.view, url_prefix="/openid")

  from ProdManager.helpers.jinja2 import (
    ternary, format_column_name, format_timeline_date,
    format_template_name, is_it_winter, include_file
  )
  from ProdManager.helpers.pagination import url_for_paginated
  from ProdManager.helpers.links import custom_url_for
  from ProdManager.helpers.lang.tools import text
  from ProdManager.helpers.stats import get_resource_view

  app.jinja_env.filters['ternary'] = ternary
  app.jinja_env.filters['format_column_name'] = format_column_name
  app.jinja_env.filters['format_timeline_date'] = format_timeline_date
  app.jinja_env.filters['format_template_name'] = format_template_name
  app.jinja_env.globals['url_for_paginated'] = url_for_paginated
  app.jinja_env.globals['custom_url_for'] = custom_url_for
  app.jinja_env.globals['_'] = text
  app.jinja_env.globals['is_it_winter'] = is_it_winter
  app.jinja_env.globals['get_resource_view'] = get_resource_view
  app.jinja_env.globals['include_file'] = include_file
  app.jinja_env.globals['git_project_url'] = GIT_PROJECT_URL
  app.jinja_env.globals['app_version'] = app.version

  app.hello = Hello(app)

  return app
