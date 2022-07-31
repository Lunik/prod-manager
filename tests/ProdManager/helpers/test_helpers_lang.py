from datetime import datetime

from ProdManager.helpers.lang.tools import text

def test_ternary():
  assert text("dashboard_title") == "Dashboard"
  assert text("dashboard_title", 2) == "Dashboards"
