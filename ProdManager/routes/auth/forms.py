from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import DataRequired

class AuthLoginForm(FlaskForm):
  secret = PasswordField(
    name='secret',
    label="secret",
    validators=[DataRequired()],
  )
