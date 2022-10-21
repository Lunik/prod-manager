from flask import current_app, g

from ProdManager.plugins import csrf

def validate_csrf():
  if current_app.config['WTF_CSRF_ENABLED'] and not g.api:
    csrf.protect()

def retreiv_username():
  if g.logged:
    if g.jwt:
      return g.jwt['aud']
    
    return 'admin'

  return None

def add_security_headers(response):
  response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
  response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline'"
  response.headers['X-Content-Type-Options'] = 'nosniff'


  username = retreiv_username()
  if username is not None:
    response.headers['X-Username'] = username

  return response
