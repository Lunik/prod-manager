from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField
from wtforms.validators import DataRequired

from ProdManager import lang

class AuthLoginForm(FlaskForm):
  secret = PasswordField(
    name='secret',
    label=lang.get("auth_form_secret").capitalize(),
    validators=[DataRequired()],
  )
  remember_me = BooleanField(
    name='remember_me',
    label=lang.get("table_column_remember_me").capitalize(),
    validators=[]
  )
