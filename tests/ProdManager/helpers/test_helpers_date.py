
from datetime import datetime

from flask import g

from ProdManager.helpers.date import (
  current_date, beautifull_date,
)

from ProdManager import create_app

app = create_app(scheduled_jobs=False)


def test_current_date():
  d = current_date()
  assert d.second == 0
  assert d.microsecond == 0


def test_beautifull_date():
  date = datetime(year=2021, month=1, day=23, hour=7, minute=11, second=59)

  with app.app_context():
    g.api = False
    assert beautifull_date(date) == "23/01/2021 07:11"

  with app.app_context():
    g.api = True
    assert beautifull_date(date) == "2021-01-23T07:11"