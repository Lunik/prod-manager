
from flask_wtf import FlaskForm
from flask import current_app, g

def strip_input(content):
  if content is None:
    return content

  if not isinstance(content, str):
    raise Exception(f"Type not handled : {content.__class__.__name__}")

  result = []
  for line in content.split('\n'):
    line = line.strip()
    if line != "":
      result.append(line)

  return '\n'.join(result)

class CustomForm(FlaskForm):
  def __init__(self, *args, **kwargs):
    super().__init__(
      meta=dict(
        csrf=current_app.config['WTF_CSRF_ENABLED'] and not g.api
      ), *args, **kwargs
    )
