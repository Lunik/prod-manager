
from ProdManager.helpers.model import (
  ModelEnum,
)

import enum


class _TestObj:
  name = "failed"

class _TestEnum(ModelEnum):
  VALUE1 = "value1"
  VALUE2 = "value2"



def test_model_enum():
  assert _TestEnum.choices() == [("value1", "VALUE1"), ("value2", "VALUE2")]

  assert _TestEnum.coerce(_TestEnum.VALUE1) == "value1"
  assert _TestEnum.coerce("value1") == "value1"

  assert _TestEnum.VALUE1 < _TestEnum.VALUE2
  assert _TestEnum.VALUE2 > _TestEnum.VALUE1
  assert _TestEnum.VALUE1 == _TestEnum.VALUE1
