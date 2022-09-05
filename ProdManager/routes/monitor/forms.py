
from wtforms import StringField, URLField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Optional, URL

from ProdManager.models import MonitorStatus

from ProdManager import lang
from ProdManager.helpers.form import CustomForm

class MonitorCreateForm(CustomForm):
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
  integration = StringField(
    name='integration',
    label=lang.get("table_column_integration").capitalize(),
    validators=[Optional()]
  )
  external_reference = StringField(
    name='external_reference',
    label=lang.get("table_column_external_reference").capitalize(),
    validators=[Optional()]
  )
  external_link = URLField(
    name='external_link',
    label=lang.get("table_column_external_link").capitalize(),
    validators=[Optional(), URL(require_tld=False)]
  )

class MonitorUpdateForm(MonitorCreateForm):
  status = SelectField(
    name='status',
    label=lang.get("table_column_status").capitalize(),
    validators=[DataRequired()],
    choices=MonitorStatus.choices(),
    coerce=MonitorStatus.coerce,
  )

class MonitorDeleteForm(CustomForm):
  pass
