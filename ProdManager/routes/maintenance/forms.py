
from wtforms import (
  StringField, TextAreaField, SelectField,
  DateTimeLocalField, BooleanField, URLField,
)
from wtforms.validators import DataRequired, Length, Optional, URL

from ProdManager.helpers.date import current_date, DATETIME_FORMAT

from ProdManager.models import (
  MaintenanceStatus, ServiceStatus,
)

from ProdManager.plugins import lang
from ProdManager.helpers.form import CustomForm

class MaintenanceCreateForm(CustomForm):
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
    validators=[Optional()],
    render_kw=dict(placeholder=lang.get("placeholder_input_description").capitalize())
  )
  external_reference= StringField(
    name='external_reference',
    label=lang.get("table_column_external_reference").capitalize(),
    validators=[Optional()]
  )
  external_link = URLField(
    name='external_link',
    label=lang.get("table_column_external_link").capitalize(),
    validators=[Optional(), URL(require_tld=False)]
  )
  service_status = SelectField(
    name='service_status',
    label=lang.get("table_column_service_status").capitalize(),
    validators=[DataRequired()],
    choices=ServiceStatus.choices(),
    coerce=ServiceStatus.coerce,
  )
  scheduled_start_date = DateTimeLocalField(
    name='scheduled_start_date',
    label=lang.get("table_column_scheduled_start_date").capitalize(),
    default=current_date,
    validators=[DataRequired()],
    format=DATETIME_FORMAT,
  )
  scheduled_end_date = DateTimeLocalField(
    name='scheduled_end_date',
    label=lang.get("table_column_scheduled_end_date").capitalize(),
    default=current_date,
    validators=[DataRequired()],
    format=DATETIME_FORMAT,
  )

class MaintenanceUpdateForm(MaintenanceCreateForm):
  status = SelectField(
    name='status',
    label=lang.get("table_column_status").capitalize(),
    validators=[DataRequired()],
    choices=MaintenanceStatus.choices(),
    coerce=MaintenanceStatus.coerce,
  )
  start_date = DateTimeLocalField(
    name='start_date',
    label=lang.get("table_column_start_date").capitalize(),
    validators=[Optional()],
    format=DATETIME_FORMAT,
  )
  end_date = DateTimeLocalField(
    name='end_date',
    label=lang.get("table_column_end_date").capitalize(),
    validators=[Optional()],
    format=DATETIME_FORMAT,
  )

class MaintenanceCommentForm(CustomForm):
  comment = TextAreaField(
    name='comment',
    label=lang.get("table_column_comment").capitalize(),
    validators=[DataRequired()],
    render_kw=dict(placeholder=lang.get("placeholder_input_comment").capitalize())
  )
  internal = BooleanField(
    name='internal',
    label=lang.get("table_column_internal").capitalize(),
    validators=[]
  )



class MaintenanceDeleteForm(CustomForm):
  pass
