from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import DataRequired

from ProdManager import lang

class AuthLoginForm(FlaskForm):
  secret = PasswordField(
    name='secret',
    label=lang.get("auth_form_secret").capitalize(),
    validators=[DataRequired()],
  )
