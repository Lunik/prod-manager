import re

def ternary(expr, value_a, value_b):
  return value_a if expr else value_b

def format_column_name(key):
  regex = re.compile(r'_(date)$')
  return regex.sub('', key).replace('_', ' ').capitalize()