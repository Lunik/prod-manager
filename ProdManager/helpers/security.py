from flask import current_app, g

from ProdManager.plugins import csrf

def validate_csrf():
  if current_app.config['WTF_CSRF_ENABLED'] and not g.api:
    csrf.protect()

def add_security_headers(response):
  response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
  response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline'"
  response.headers['X-Content-Type-Options'] = 'nosniff'

  return response
