from flask_wtf import FlaskForm
from wtforms import StringField, URLField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Optional, URL

from ProdManager.models.Monitor import MonitorStatus

class MonitorCreateForm(FlaskForm):
  scope_id = SelectField(name='scope', validators=[DataRequired()])
  service_id = SelectField(name='service', validators=[DataRequired()])
  name = StringField(name='name', validators=[DataRequired(), Length(min=4)])
  description = TextAreaField(name='description', validators=[Optional()])
  external_link = URLField(name='external_link', validators=[Optional(), URL()])

class MonitorUpdateForm(FlaskForm):
  scope_id = SelectField(name='scope', validators=[DataRequired()])
  service_id = SelectField(name='service', validators=[DataRequired()])
  name = StringField(name='name', validators=[DataRequired(), Length(min=4)])
  description = TextAreaField(name='description', validators=[Optional()])
  status = SelectField(
    name='status',
    validators=[DataRequired()],
    choices=MonitorStatus.choices(),
    coerce=MonitorStatus.coerce,
  )
  external_link = URLField(name='external_link', validators=[Optional(), URL()])

class MonitorDeleteForm(FlaskForm):
  pass