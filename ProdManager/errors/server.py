from flask import current_app
from ProdManager.helpers.template import custom_render_template

def internal_error(error):
  current_app.logger.debug(error)
  return custom_render_template("error/500.html",
    error=error,
    json=dict(resources=error.description, serialize=False)
  ), 500
