from flask_wtf import FlaskForm
from wtforms import EmailField
from wtforms.validators import DataRequired, Email

class SubscribeForm(FlaskForm):
  email = EmailField(name='email', validators=[DataRequired(), Email()])

class UnSubscribeForm(FlaskForm):
  email = EmailField(name='email', validators=[DataRequired(), Email()])
