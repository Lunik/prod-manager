import re

def ternary(expr, value_a, value_b):
  return value_a if expr else value_b

def format_column_name(key):
  regex = re.compile(r'_(date)$')
  return regex.sub('', key).replace('_', ' ').capitalize()

def format_timeline_date(date, orientation="horizontal"):
  if orientation == "horizontal":
    date = date.strftime('%d/%m/%Y %H:%M')
  elif orientation == "vertical":
    date = date.strftime('%d/%m/%Y TODO %H:%M')
  else:
    date = date.strftime('%d/%m/%Y at %H:%M')

  return date
