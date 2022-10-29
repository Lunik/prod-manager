from datetime import datetime, timedelta

from wtforms import DateTimeLocalField, PasswordField, StringField, SelectMultipleField
from wtforms.validators import DataRequired, Length

from ProdManager.plugins import lang
from ProdManager.helpers.form import CustomForm

class TokenCreateForm(CustomForm):
  secret = PasswordField(
    name='secret',
    label=lang.get("table_column_secret").capitalize(),
    validators=[DataRequired()],
  )
  name = StringField(
    name='name',
    label=lang.get("table_column_name").capitalize(),
    validators=[DataRequired(), Length(min=8, max=16)]
  )
  description = StringField(
    name='description',
    label=lang.get("table_column_description").capitalize(),
    validators=[DataRequired(), Length(min=12, max=32)]
  )
  not_before_date = DateTimeLocalField(
    name='not_before_date',
    label=lang.get("table_column_not_before_date").capitalize(),
    default=datetime.utcnow(),
    validators=[DataRequired()],
    format='%Y-%m-%dT%H:%M',
  )
  expiration_date = DateTimeLocalField(
    name='expiration_date',
    label=lang.get("table_column_expiration_date").capitalize(),
    default=datetime.utcnow() + timedelta(hours=1),
    validators=[DataRequired()],
    format='%Y-%m-%dT%H:%M',
  )
  permissions = SelectMultipleField(
    name='permissions',
    label=lang.get("table_column_permissions").capitalize(),
    default=[],
    validators=[],
  )
