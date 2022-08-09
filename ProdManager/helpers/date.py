from datetime import datetime

from flask import g

def current_date(rounded=True):
  date = datetime.now()

  if rounded:
    date = date.replace(second=0, microsecond=0)

  return date

def beautifull_date(date):
  if g.api:
    return date.strftime('%Y-%m-%dT%H:%M')

  return date.strftime('%d/%m/%Y %H:%M')
