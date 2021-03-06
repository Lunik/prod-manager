from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

from ProdManager import lang

class ScopeCreateForm(FlaskForm):
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

class ScopeUpdateForm(ScopeCreateForm):
  pass

class ScopeDeleteForm(FlaskForm):
  pass
