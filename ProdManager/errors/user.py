from werkzeug.exceptions import BadRequest
from flask_wtf.csrf import CSRFError

from flask import current_app
from ProdManager.helpers.template import custom_render_template

def page_not_found(error):
  current_app.logger.debug(error)
  return custom_render_template("error/404.html",
    error=error
  ), 404

def conflict(error):
  current_app.logger.debug(error)
  return custom_render_template("error/409.html",
    error=error
  ), 409

def forbiden(error):
  current_app.logger.debug(error)
  return custom_render_template("error/403.html",
    error=error
  ), 403

def bad_request(error):
  if isinstance(error, CSRFError):
    error = BadRequest(description=dict(
      message="Invalid request",
      reasons=dict(csrf=[error.description]),
    ))

  current_app.logger.debug(error)
  return custom_render_template("error/400.html",
    error=error
  ), 400
