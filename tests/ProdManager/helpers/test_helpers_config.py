
from ProdManager.helpers.config import (
  boolean_param,
)


def test_boolean_param():
  assert boolean_param("true")
  assert boolean_param("t")
  assert boolean_param("1")
  assert boolean_param("True")
  assert boolean_param("TRUE")
  assert not boolean_param("false")
  assert not boolean_param("False")
  assert not boolean_param("0")
  assert not boolean_param("tralala")
  assert not boolean_param("-1")
  assert not boolean_param("2")
