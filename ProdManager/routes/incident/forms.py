
from wtforms import (
  StringField, TextAreaField, SelectField,
  DateTimeLocalField, BooleanField, URLField,
)
from wtforms.validators import DataRequired, Length, Optional, URL

from ProdManager.helpers.date import current_date

from ProdManager.models import IncidentSeverity, IncidentStatus

from ProdManager import lang
from ProdManager.helpers.form import CustomForm

class IncidentCreateForm(CustomForm):
  scope = SelectField(
    name='scope',
    label=lang.get("table_column_scope").capitalize(),
    validators=[DataRequired()]
  )
  service = SelectField(
    name='service',
    label=lang.get("table_column_service").capitalize(),
    validators=[DataRequired()]
  )
  name = StringField(
    name='name',
    label=lang.get("table_column_name").capitalize(),
    validators=[DataRequired(), Length(min=4)]
  )
  description = TextAreaField(
    name='description',
    label=lang.get("table_column_description").capitalize(),
    validators=[Optional()]
  )
  external_reference= StringField(
    name='external_reference',
    label=lang.get("table_column_external_reference").capitalize(),
    validators=[Optional()]
  )
  external_link = URLField(
    name='external_link',
    label=lang.get("table_column_external_link").capitalize(),
    validators=[Optional(), URL()]
  )
  severity = SelectField(
    name='severity',
    label=lang.get("table_column_severity").capitalize(),
    validators=[DataRequired()],
    choices=IncidentSeverity.choices(),
    coerce=IncidentSeverity.coerce,
  )
  start_impact_date = DateTimeLocalField(
    name='start_impact_date',
    label=lang.get("table_column_start_impact_date").capitalize(),
    default=current_date,
    validators=[DataRequired()],
    format='%Y-%m-%dT%H:%M',
  )

class IncidentUpdateForm(IncidentCreateForm):
  status = SelectField(
    name='status',
    label=lang.get("table_column_status").capitalize(),
    validators=[DataRequired()],
    choices=IncidentStatus.choices(),
    coerce=IncidentStatus.coerce,
  )
  investigation_date = DateTimeLocalField(
    name='investigation_date',
    label=lang.get("table_column_investigation_date").capitalize(),
    validators=[Optional()],
    format='%Y-%m-%dT%H:%M',
  )
  stable_date = DateTimeLocalField(
    name='stable_date',
    label=lang.get("table_column_stable_date").capitalize(),
    validators=[Optional()],
    format='%Y-%m-%dT%H:%M',
  )
  resolve_date = DateTimeLocalField(
    name='resolve_date',
    label=lang.get("table_column_resolve_date").capitalize(),
    validators=[Optional()],
    format='%Y-%m-%dT%H:%M',
  )

class IncidentCommentForm(CustomForm):
  comment = TextAreaField(
    name='comment',
    label=lang.get("table_column_comment").capitalize(),
    validators=[DataRequired()]
  )
  internal = BooleanField(
    name='internal',
    label=lang.get("table_column_internal").capitalize(),
    validators=[]
  )

class IncidentDeleteForm(CustomForm):
  pass
