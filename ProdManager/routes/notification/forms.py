
from wtforms import EmailField
from wtforms.validators import DataRequired, Email

from ProdManager.plugins import lang
from ProdManager.helpers.form import CustomForm

class SubscribeForm(CustomForm):
  email = EmailField(
    name='email',
    label=lang.get("table_column_mail").capitalize(),
    validators=[DataRequired(), Email()]
  )

class UnSubscribeForm(SubscribeForm):
  pass
