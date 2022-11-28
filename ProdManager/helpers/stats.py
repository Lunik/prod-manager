
from redis import exceptions as redis_exceptions
from flask import current_app, request

from ProdManager.plugins import redis_client

def get_resource_view():
  if not current_app.config['STATS_ENABLED']:
    return None

  key = f"stats/resource/view/_{request.path}"

  try:
    views = redis_client.incr(key)
  except redis_exceptions.ConnectionError as error:
    current_app.logger.error(
      "Unable get resource view stats because Redis instance is unreachable : %s", error)
    return None
  except redis_exceptions.ResponseError as error:
    current_app.logger.error(
      "Unable get resource view stats because of an error : %s", error)
    return None

  # Use `format` function to display view count with `,` on thousands
  # 1000000 => 1,000,000
  return format(views, ',')
