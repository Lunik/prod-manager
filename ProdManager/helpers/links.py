from flask import url_for, g

# Required to render full URLs in emails templates
def custom_url_for(endpoint, *args, **kwargs):
  raw = endpoint.split('.')

  blueprint_name = raw[0]
  route_name = raw[1] if len(raw) > 1 else None

  if g.api and "api" not in blueprint_name:
    endpoint = f"{blueprint_name}_api"
    if route_name:
      endpoint += f".{route_name}"

  return url_for(
    endpoint,
    *args,
    _external=True,
    **kwargs,
  )
