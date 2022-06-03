from datetime import datetime, timedelta

from flask_wtf import FlaskForm
from wtforms import PasswordField, DateTimeLocalField
from wtforms.validators import DataRequired

class AuthTokenForm(FlaskForm):
  secret = PasswordField(
    name='secret',
    label="secret",
    validators=[DataRequired()],
  )
  expiration = DateTimeLocalField(
    name='expiration',
    label="expiration",
    default=datetime.now() + timedelta(days=1),
    validators=[DataRequired()],
    format='%Y-%m-%dT%H:%M'
  )

class AuthLoginForm(FlaskForm):
  token = PasswordField(
    name='token',
    label="token",
    validators=[DataRequired()],
  )
