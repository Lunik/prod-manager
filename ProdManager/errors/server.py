from flask import current_app, render_template

def internal_error(error):
  current_app.logger.debug(error)
  return render_template("error/500.html",
    error=error
  ), 500
