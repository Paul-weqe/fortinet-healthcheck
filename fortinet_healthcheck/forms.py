from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, RadioField, SelectField
from wtforms.validators import DataRequired
from wtforms.widgets import PasswordInput, NumberInput

INPUT_KW = {
    'class': 'form-control'
}

SELECT_KW = {
    'class': 'form-select',
    'aria-label': 'Default select example'
}

NETMIKO_ALIAS_KW = INPUT_KW
NETMIKO_ALIAS_KW['aria-describedby'] = "passwordHelpBlock"


class CreateDeviceForm(FlaskForm):
    alias = StringField('Device Name', validators=[DataRequired()], render_kw=INPUT_KW)
    hostname = StringField('Device hostname/IP', validators=[DataRequired()], render_kw=INPUT_KW)
    username = StringField('Device username', validators=[DataRequired()], render_kw=INPUT_KW)
    password = StringField('Device password',
                           widget=PasswordInput(), render_kw=INPUT_KW
                           )
    vendor = SelectField('Vendor', choices=[], render_kw=SELECT_KW)
    port = IntegerField('Port', widget=NumberInput(step=1, min=1, max=65_535), render_kw=INPUT_KW, default=22)


class OutputEntryForm(FlaskForm):
    name = StringField('', render_kw=INPUT_KW)


class CreateHealthCheckForm(FlaskForm):
    CHECK_TYPE_OPTIONS = [
        ('and', 'AND'),
        ('or', 'OR'),
        ('not', 'NOT')
    ]
    
    name = StringField('Name', validators=[DataRequired()], render_kw=INPUT_KW)
    command = StringField('Command', validators=[DataRequired()], render_kw=INPUT_KW)
    check_type = RadioField('Check Type', choices=CHECK_TYPE_OPTIONS, default=CHECK_TYPE_OPTIONS[0][0], render_kw={
        'class': 'checkbox-check-type'
    })
    vendor = SelectField('Vendor', choices=[], render_kw=SELECT_KW)
    check_result = TextAreaField('Check Results', render_kw=INPUT_KW)
    description = TextAreaField('Description', render_kw=INPUT_KW)

class CreateVendorForm(FlaskForm):
    vendor_name = StringField('Vendor Name', validators=[DataRequired()], render_kw=INPUT_KW)
    netmiko_alias = StringField('Netmiko Alias', validators=[DataRequired()], render_kw=NETMIKO_ALIAS_KW)
