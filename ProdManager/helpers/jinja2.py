import re
import logging
from datetime import datetime
from flask import current_app

from ProdManager.helpers.date import beautifull_date

logger = logging.getLogger('gunicorn.error')

def ternary(expr, value_a, value_b):
  return value_a if expr else value_b

def format_column_name(key):
  regex = re.compile(r'_(date)$')
  return regex.sub('', key).replace('_', ' ').capitalize()

def format_timeline_date(date):
  return beautifull_date(date) if isinstance(date, datetime) else ''

def format_template_name(key, keep="folder"):
  if keep == "folder":
    return key.split('/')[0]

  return key

winter_dates = (datetime(datetime.now().year, 12, 1), datetime(datetime.now().year + 1, 1, 31))
summer_dates = (datetime(datetime.now().year, 6, 1), datetime(datetime.now().year, 8, 31))

def is_it(season):
  if season == "winter":
    now = datetime.utcnow()
    return now >= winter_dates[0] and now <= winter_dates[1]
  elif season == "summer":
    now = datetime.utcnow()
    return now >= summer_dates[0] and now <= summer_dates[1]

  return False

def include_file(name):
  content = b""

  try:
    with current_app.open_resource(name) as file:
      content = file.read()
  except Exception as error:
    logger.error(error)

  return content.decode('UTF-8')
