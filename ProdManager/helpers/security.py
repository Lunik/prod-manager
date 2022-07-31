from flask import current_app, g

from ProdManager import csrf

def validate_csrf():
  if current_app.config['WTF_CSRF_ENABLED'] and not g.api:
    csrf.protect()
