
class ViewException(Exception):
  def __init__(self, message, reasons, http_code):
    super().__init__(message)

    self.message = message
    self.reasons = reasons
    self.http_code = http_code

  @property
  def error(self):
    return dict(message=self.message, reasons=self.reasons)
