
import pytest
import enum
from datetime import datetime

from flask import g

from ProdManager.helpers.json import (
  json_defaults,
)

from ProdManager import create_app

app = create_app(scheduled_jobs=False)


class _TestObj:
  name = "failed"

class _TestEnum(enum.Enum):
  VALUE1 = "value1"
  VALUE2 = "value2"


def test_json_defaults():
  date = datetime(year=2021, month=1, day=23, hour=7, minute=11, second=59)
  with app.app_context():
    g.api = False
    assert json_defaults(date) == "23/01/2021 07:11"

  with app.app_context():
    g.api = True
    assert json_defaults(date) == "2021-01-23T07:11"

  assert json_defaults(_TestEnum.VALUE1) == "VALUE1"

  with pytest.raises(Exception):
    json_defaults(_TestObj())
