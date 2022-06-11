from datetime import timedelta

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeLocalField
from wtforms.validators import DataRequired, Length, Optional

from ProdManager.helpers.date import current_date

from ProdManager.models.Maintenance import MaintenanceStatus
from ProdManager.models.Service import ServiceStatus

class MaintenanceCreateForm(FlaskForm):
  scope_id = SelectField(name='scope', validators=[DataRequired()])
  service_id = SelectField(name='service', validators=[DataRequired()])
  name = StringField(name='name', validators=[DataRequired(), Length(min=4)])
  description = TextAreaField(name='description', validators=[Optional()])
  external_reference= StringField(name='external_reference', validators=[Optional()])
  service_status = SelectField(
    name='service status',
    validators=[DataRequired()],
    choices=ServiceStatus.choices(),
    coerce=ServiceStatus.coerce,
  )
  scheduled_start_date = DateTimeLocalField(
    name='scheduled start date',
    default=current_date(),
    validators=[DataRequired()],
    format='%Y-%m-%dT%H:%M',
  )
  scheduled_end_date = DateTimeLocalField(
    name='scheduled end date',
    default=current_date() + timedelta(hours=1),
    validators=[DataRequired()],
    format='%Y-%m-%dT%H:%M',
  )

class MaintenanceUpdateForm(FlaskForm):
  scope_id = SelectField(name='scope', validators=[DataRequired()])
  service_id = SelectField(name='service', validators=[DataRequired()])
  name = StringField(name='name', validators=[DataRequired(), Length(min=4)])
  description = TextAreaField(name='description', validators=[Optional()])
  external_reference= StringField(name='external_reference', validators=[Optional()])
  status = SelectField(
    name='status',
    validators=[DataRequired()],
    choices=MaintenanceStatus.choices(),
    coerce=MaintenanceStatus.coerce,
  )
  service_status = SelectField(
    name='service status',
    validators=[DataRequired()],
    choices=ServiceStatus.choices(),
    coerce=ServiceStatus.coerce,
  )
  scheduled_start_date = DateTimeLocalField(
    name='scheduled start date',
    default=current_date(),
    validators=[DataRequired()],
    format='%Y-%m-%dT%H:%M',
  )
  scheduled_end_date = DateTimeLocalField(
    name='scheduled end date',
    default=current_date() + timedelta(hours=1),
    validators=[DataRequired()],
    format='%Y-%m-%dT%H:%M',
  )

class MaintenanceCommentForm(FlaskForm):
  comment = TextAreaField(name='comment', validators=[DataRequired()])


class MaintenanceDeleteForm(FlaskForm):
  pass
