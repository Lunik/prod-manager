import re

from ProdManager.helpers.date import beautifull_date

def ternary(expr, value_a, value_b):
  return value_a if expr else value_b

def format_column_name(key):
  regex = re.compile(r'_(date)$')
  return regex.sub('', key).replace('_', ' ').capitalize()

def format_timeline_date(date):
  return beautifull_date(date)

def format_template_name(key, keep="folder"):
  if keep == "folder":
    return f"{key.split('/')[0]}s".capitalize()

  return key
