
from ProdManager.helpers.response import (
  CrudError, IncorrectValueError,
  NotFoundError, ConflictError,
  ServerError, UndeletableRessourceError,
  DependencyError,
)


def test_incorrect_value_error():
  try:
    raise IncorrectValueError("test")
  except IncorrectValueError as error:
    assert error.code == 404
    assert "test" in error.message

  try:
    raise NotFoundError("test")
  except NotFoundError as error:
    assert error.code == 404
    assert "test" in error.message

  try:
    raise ConflictError("{tralala: 'trilili'}")
  except ConflictError as error:
    assert error.code == 409
    assert "{tralala: 'trilili'}" in error.message

  try:
    raise ServerError("test")
  except ServerError as error:
    assert error.code == 500
    assert "test" in error.message

  try:
    raise UndeletableRessourceError("test")
  except UndeletableRessourceError as error:
    assert error.code == 403
    assert "test" in error.message

  try:
    raise DependencyError("test")
  except DependencyError as error:
    assert error.code == 403
    assert "test" in error.message
