from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

class ScopeCreateForm(FlaskForm):
  name = StringField(name='name', validators=[DataRequired(), Length(min=3)])
  description = TextAreaField(name='description', validators=[])

class ScopeUpdateForm(FlaskForm):
  name = StringField(name='name', validators=[DataRequired(), Length(min=3)])
  description = TextAreaField(name='description', validators=[])

class ScopeDeleteForm(FlaskForm):
  pass
