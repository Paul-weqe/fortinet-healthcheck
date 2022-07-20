from flask import Blueprint, render_template, flash, url_for, redirect
from fortinet_healthcheck.forms import CreateDeviceForm
from fortinet_healthcheck.services import devices_service

device_blueprint = Blueprint('devices_blueprint', __name__)


@device_blueprint.route("/create-device", methods=['GET', 'POST'])
def create_device():
    form = CreateDeviceForm()
    if form.validate_on_submit():
        device = devices_service.create_device(
            alias=form.alias.data, hostname=form.hostname.data, username=form.username.data,
            port=form.port.data, password=form.password.data
        )
        flash('success', f"Successfully added device {device.hostname}")
        return redirect(url_for('auth_blueprint.home_page'))
    return render_template('create-device.html', form=form)
