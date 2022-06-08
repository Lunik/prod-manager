from datetime import datetime, timedelta
from markupsafe import escape

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeLocalField
from wtforms.validators import DataRequired, Length, Optional

from ProdManager.models.Maintenance import MaintenanceStatus
from ProdManager.models.Service import ServiceStatus

class MaintenanceCreateForm(FlaskForm):
  name = StringField(name='name', validators=[DataRequired(), Length(min=4)])
  external_reference= StringField(name='external_reference', validators=[Optional()])
  scheduled_start_date = DateTimeLocalField(
    name='scheduled start date',
    default=datetime.now(),
    validators=[Optional()],
    format='%Y-%m-%dT%H:%M'
  )
  scheduled_end_date = DateTimeLocalField(
    name='scheduled end date',
    default=datetime.now() + timedelta(hours=1),
    validators=[Optional()],
    format='%Y-%m-%dT%H:%M'
  )
  service_status = SelectField(name='service status', validators=[DataRequired()], choices=ServiceStatus.choices(), coerce=ServiceStatus.coerce)
  description = TextAreaField(name='description', validators=[Optional()])
  scope_id = SelectField(name='scope', validators=[DataRequired()])
  service_id = SelectField(name='service', validators=[DataRequired()])

class MaintenanceUpdateForm(FlaskForm):
  name = StringField(name='name', validators=[DataRequired(), Length(min=4)])
  external_reference= StringField(name='external_reference', validators=[Optional()])
  status = SelectField(name='status', validators=[DataRequired()], choices=MaintenanceStatus.choices(), coerce=MaintenanceStatus.coerce)
  scheduled_start_date = DateTimeLocalField(
    name='scheduled start date',
    default=datetime.now(),
    validators=[Optional()],
    format='%Y-%m-%dT%H:%M'
  )
  scheduled_end_date = DateTimeLocalField(
    name='scheduled end date',
    default=datetime.now() + timedelta(hours=1),
    validators=[Optional()],
    format='%Y-%m-%dT%H:%M'
  )
  start_date = DateTimeLocalField(
    name='start date',
    validators=[Optional()],
    format='%Y-%m-%dT%H:%M'
  )
  end_date = DateTimeLocalField(
    name='end date',
    validators=[Optional()],
    format='%Y-%m-%dT%H:%M'
  )
  service_status = SelectField(name='service status', validators=[DataRequired()], choices=ServiceStatus.choices(), coerce=ServiceStatus.coerce)
  description = TextAreaField(name='description', validators=[Optional()])
  scope_id = SelectField(name='scope', validators=[DataRequired()])
  service_id = SelectField(name='service', validators=[DataRequired()])

class MaintenanceDeleteForm(FlaskForm):
  pass
