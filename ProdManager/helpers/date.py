from datetime import datetime

def current_date(rounded=True):
  date = datetime.now()

  if rounded:
    date = date.replace(second=0, microsecond=0)

  return date

def beautifull_date(date):
  return date.strftime('%d/%m/%Y %H:%M')