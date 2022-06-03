from .view import ViewException

class UserException(ViewException):
  def __init__(self, reasons, http_code, message="User exception"):
    super().__init__(message=message, reasons=reasons, http_code=http_code)
