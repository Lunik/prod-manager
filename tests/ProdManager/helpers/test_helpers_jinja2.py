from datetime import datetime

from flask import g

from ProdManager.helpers.jinja2 import (
  ternary, format_column_name, format_timeline_date,
  format_template_name,
)

from ProdManager import create_app

app = create_app(scheduled_jobs=False)


def test_ternary():
  assert ternary(True, "value1", "value2") == "value1"
  assert ternary(False, "value1", "value2") == "value2"
  assert ternary(None, "value1", "value2") == "value2"
  assert ternary("", "value1", "value2") == "value2"
  assert ternary(0, "value1", "value2") == "value2"
  assert ternary(1, "value1", "value2") == "value1"


def test_format_column_name():
  assert format_column_name("tralala") == "Tralala"
  assert format_column_name("tralala_date") == "Tralala"
  assert format_column_name("tralala_data") == "Tralala data"
  assert format_column_name("tralala_date_ok") == "Tralala date ok"

  assert format_column_name("a b c") == "A b c"
  assert format_column_name("a_b c") == "A b c"
  assert format_column_name("a_b_c__") == "A b c  "


def test_format_timeline_date():
  date = datetime(year=2021, month=1, day=23, hour=7, minute=11, second=59)

  with app.app_context():
    g.api = False
    assert format_timeline_date(date) == "23/01/2021 07:11"

  with app.app_context():
    g.api = True
    assert format_timeline_date(date) == "2021-01-23T07:11"

  with app.app_context():
    g.api = False
    assert format_timeline_date(None) == ""


def test_format_template_name():
  assert format_template_name("monitor/tralala.html") == "monitor"
  assert format_template_name("monitor/trululu/tralala.html") == "monitor"
  assert format_template_name("monitor/tralala.html", keep=False) == "monitor/tralala.html"
