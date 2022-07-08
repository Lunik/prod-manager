from datetime import datetime

from ProdManager.filters.lang import text

def test_ternary():
  assert text("dashboard_title") == "Dashboard"
  assert text("dashboard_title", 2) == "Dashboards"
