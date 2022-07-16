from flask import url_for

# Required to render full URLs in emails templates
def custom_url_for(endpoint, *args, **kwargs):
  return url_for(
    endpoint,
    *args,
    _external=True,
    **kwargs,
  )
