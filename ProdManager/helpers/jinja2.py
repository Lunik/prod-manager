import re
from datetime import datetime

from ProdManager.helpers.date import beautifull_date

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

def is_it_winter():
  now = datetime.utcnow()
  return now >= winter_dates[0] and now <= winter_dates[1]