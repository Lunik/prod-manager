from datetime import datetime

from flask import g

DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M'
READABLE_DATETIME_FORMAT = '%d/%m/%Y %H:%M'

def current_date(rounded=True):
  date = datetime.now()

  if rounded:
    date = date.replace(second=0, microsecond=0)

  return date

def beautifull_date(date):
  if g.api:
    return date.strftime(DATETIME_FORMAT)

  return date.strftime(READABLE_DATETIME_FORMAT)
