from flask import jsonify

class CrudError(Exception):
  def __init__(self, message, code):
    self.message = message
    self.code = code

  def render(self):
    return jsonify(dict(
      self.message
    )), self.code

class IncorrectValueError(CrudError):
  def __init__(self, identifier):
    super().__init__(f"Incorrect value for attribute : {identifier}", 404)

class NotFoundError(CrudError):
  def __init__(self, identifier):
    super().__init__(f"Resource not found : {identifier}", 404)

class ConflictError(CrudError):
  def __init__(self, attributs):
    super().__init__(f"Conflict on resource with attributes : {attributs}", 409)

class ServerError(CrudError):
  def __init__(self, error):
    super().__init__(error, 500)

class UndeletableRessourceError(CrudError):
  def __init__(self, error):
    super().__init__(error, 403)

class DependencyError(CrudError):
  def __init__(self, error):
    super().__init__(error, 403)
