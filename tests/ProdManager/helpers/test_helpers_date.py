
from datetime import datetime

from ProdManager.helpers.date import (
  current_date, beautifull_date,
)


def test_current_date():
  d = current_date()
  assert d.second == 0
  assert d.microsecond == 0


def test_beautifull_date():
  date = datetime(year=2021, month=1, day=23, hour=7, minute=11, second=59)
  assert beautifull_date(date) == "23/01/2021 07:11"
