from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeLocalField
from wtforms.validators import DataRequired, Length, Optional

from ProdManager.models.Incident import IncidentSeverity, IncidentStatus

class IncidentCreateForm(FlaskForm):
  scope_id = SelectField(name='scope', validators=[DataRequired()])
  service_id = SelectField(name='service', validators=[DataRequired()])
  name = StringField(name='name', validators=[DataRequired(), Length(min=4)])
  description = TextAreaField(name='description', validators=[Optional()])
  external_reference= StringField(name='external_reference', validators=[Optional()])
  severity = SelectField(
    name='severity',
    validators=[DataRequired()],
    choices=IncidentSeverity.choices(),
    coerce=IncidentSeverity.coerce,
  )
  start_impact_date = DateTimeLocalField(
    name='start impact date',
    default=datetime.now(),
    validators=[Optional()],
    format='%Y-%m-%dT%H:%M',
  )

class IncidentUpdateForm(FlaskForm):
  scope_id = SelectField(name='scope', validators=[DataRequired()])
  service_id = SelectField(name='service', validators=[DataRequired()])
  name = StringField(name='name', validators=[DataRequired(), Length(min=4)])
  description = TextAreaField(name='description', validators=[Optional()])
  external_reference= StringField(name='external_reference', validators=[Optional()])
  severity = SelectField(
    name='severity',
    validators=[DataRequired()],
    choices=IncidentSeverity.choices(),
    coerce=IncidentSeverity.coerce,
    )
  status = SelectField(
    name='status',
    validators=[DataRequired()],
    choices=IncidentStatus.choices(),
    coerce=IncidentStatus.coerce,
    )
  start_impact_date = DateTimeLocalField(
    name='start impact date',
    default=datetime.now(),
    validators=[Optional()],
    format='%Y-%m-%dT%H:%M',
  )

class IncidentDeleteForm(FlaskForm):
  pass
