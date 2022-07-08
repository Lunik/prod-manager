from flask_wtf import FlaskForm
from wtforms import EmailField
from wtforms.validators import DataRequired, Email

from ProdManager import lang

class SubscribeForm(FlaskForm):
  email = EmailField(
    name='email',
    label=lang.get("table_column_mail").capitalize(),
    validators=[DataRequired(), Email()]
  )

class UnSubscribeForm(SubscribeForm):
  pass
