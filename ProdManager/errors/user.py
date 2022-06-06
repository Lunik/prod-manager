from flask import current_app, render_template

def error_404(description):
  current_app.logger.debug(description)
  return render_template("error/404.html",
    error=description
  ), 404
