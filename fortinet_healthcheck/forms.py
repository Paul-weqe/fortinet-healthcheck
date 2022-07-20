from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators, TextAreaField, RadioField
from wtforms.validators import DataRequired
from wtforms.widgets import PasswordInput, NumberInput


class CreateDeviceForm(FlaskForm):
    alias = StringField('Device Name: ', validators=[DataRequired()])
    hostname = StringField('device hostname/IP:', validators=[DataRequired()])
    username = StringField('device username:', validators=[DataRequired()])
    password = StringField('device password:',
                           widget=PasswordInput(),
                           validators=[DataRequired()]
                           )
    port = IntegerField('port', widget=NumberInput(step=1, min=1, max=65_535))


class CreateHealthCheckForm(FlaskForm):
    CHECK_TYPE_OPTIONS = [
        ('and', 'AND'),
        ('or', 'OR'),
        ('not', 'NOT')
    ]

    name = StringField('Name', validators=[DataRequired()])
    command = StringField('Command', validators=[DataRequired()])
    check_type = RadioField('Check Type', choices=CHECK_TYPE_OPTIONS, default=CHECK_TYPE_OPTIONS[0][0])
    description = TextAreaField('Description')


