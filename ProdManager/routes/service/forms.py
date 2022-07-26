
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

from ProdManager import lang
from ProdManager.helpers.form import CustomForm

class ServiceCreateForm(CustomForm):
  name = StringField(
    name='name',
    label=lang.get("table_column_name").capitalize(),
    validators=[DataRequired(), Length(min=3)]
  )
  description = TextAreaField(
    name='description',
    label=lang.get("table_column_description").capitalize(),
    validators=[Optional()]
  )

class ServiceUpdateForm(ServiceCreateForm):
  pass

class ServiceDeleteForm(CustomForm):
  pass
