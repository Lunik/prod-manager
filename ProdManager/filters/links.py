from flask import url_for, current_app

# Required to render full URLs in emails templates
def custom_url_for(endpoint, *args, **kwargs):
  return url_for(
    endpoint,
    *args,
    _external=True,
    _scheme=current_app.config["PREFERRED_URL_SCHEME"],
    **kwargs,
  )
