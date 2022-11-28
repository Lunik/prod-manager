import re
import hashlib
from redis import exceptions as redis_exceptions

from flask import request, g, current_app, abort
from ProdManager.plugins import lang, redis_client

api_path_regex = re.compile(r'^/api/.*')

def retreiv_api():
  g.api = api_path_regex.match(request.path) is not None

def get_client_key():
  if g.jwt:
    client_id = g.jwt['jti']
  else:
    client_id = request.remote_addr
    if g.logged:
      client_id = f"{client_id}/logged"

  client_key = hashlib.sha256(client_id.encode('utf-8')).hexdigest()

  return client_key

def get_api_ratelimit():
  if g.logged:
    return current_app.config['API_RATELIMIT_LOGGED']

  return current_app.config['API_RATELIMIT_DEFAULT']

def get_ratelimit_expire():
  return current_app.config['API_RATELIMIT_PERIOD_HOURS'] * 3600

def get_ratelimit():
  client_key = get_client_key()

  key = f"api/ratelimit/{client_key}"
  pipe = redis_client.pipeline()

  pipe.incr(key)
  pipe.expire(key, get_ratelimit_expire(), lt=True)
  pipe.expiretime(key)
  pipe.ttl(key)

  res = pipe.execute()

  return dict(
    client_key=client_key,
    limit=get_api_ratelimit(),
    value=res[0],
    reset=res[2],
    ttl=res[3]
  )

def validate_ratelimit_api():
  if not g.api or not current_app.config['API_RATELIMIT_ENABLED']:
    return

  g.ratelimit = None

  # Decreasing ratelimit remaining
  try:
    g.ratelimit = get_ratelimit()
  except redis_exceptions.ConnectionError as error:
    current_app.logger.error(
      "Unable to verify API rates limit because Redis instance is unreachable : %s", error)
    return

  if g.ratelimit['value'] <= g.ratelimit['limit']:
    # API access authorized
    return

  # User have reached ratelimit doesn't have any remaining queries
  # He must wait until the reset date
  abort(429, dict(
    message=lang.get("api_ratelimit_reached")
  ))


def add_ratelimit_api_headers(response):
  if not g.api or not current_app.config['API_RATELIMIT_ENABLED']:
    return response

  if g.ratelimit is None:
    return response

  response.headers['X-RateLimit-Client'] = g.ratelimit['client_key']
  response.headers['X-RateLimit-Limit'] = g.ratelimit['limit']
  response.headers['X-RateLimit-Reset'] = g.ratelimit['reset']
  response.headers['X-RateLimit-Remaining'] = max(0, (g.ratelimit['limit'] - g.ratelimit['value']))
  response.headers['X-RateLimit-Used'] = min(g.ratelimit['limit'], g.ratelimit['value'])

  if response.status_code == 429:
    response.headers['Retry-After'] = g.ratelimit['ttl']

  return response
