from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length

from ProdManager.models.Service import ServiceStatus

class ServiceCreateForm(FlaskForm):
  name = StringField(name='name', validators=[DataRequired(), Length(min=3)])
  description = TextAreaField(name='description', validators=[])

class ServiceUpdateForm(FlaskForm):
  name = StringField(name='name', validators=[DataRequired(), Length(min=3)])
  description = TextAreaField(name='description', validators=[])
  status = SelectField(name='status', validators=[DataRequired()], choices=ServiceStatus.choices(), coerce=ServiceStatus.coerce)

class ServiceDeleteForm(FlaskForm):
  pass
