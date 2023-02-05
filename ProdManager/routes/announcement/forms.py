
from wtforms import (
  StringField, TextAreaField, SelectField,
  DateTimeLocalField,
)
from wtforms.validators import DataRequired, Length, Optional

from ProdManager.helpers.date import current_date, DATETIME_FORMAT

from ProdManager.models import (
  AnnouncementLevel,
)

from ProdManager.plugins import lang
from ProdManager.helpers.form import CustomForm

class AnnouncementCreateForm(CustomForm):
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
  level = SelectField(
    name='level',
    label=lang.get("table_column_level").capitalize(),
    validators=[DataRequired()],
    choices=AnnouncementLevel.choices(),
    coerce=AnnouncementLevel.coerce,
  )
  start_date = DateTimeLocalField(
    name='start_date',
    label=lang.get("table_column_start_date").capitalize(),
    default=current_date,
    validators=[DataRequired()],
    format=DATETIME_FORMAT,
  )
  end_date = DateTimeLocalField(
    name='end_date',
    label=lang.get("table_column_end_date").capitalize(),
    default=current_date,
    validators=[DataRequired()],
    format=DATETIME_FORMAT,
  )

class AnnouncementUpdateForm(AnnouncementCreateForm):
  pass

class AnnouncementDeleteForm(CustomForm):
  pass
