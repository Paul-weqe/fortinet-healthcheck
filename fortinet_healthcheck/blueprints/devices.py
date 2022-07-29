from flask import Blueprint, render_template, flash, url_for, redirect
from fortinet_healthcheck.forms import CreateDeviceForm
from fortinet_healthcheck.services import health_check_service, devices_service
from fortinet_healthcheck.services.devices_service import get_all_devices

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


@device_blueprint.route("/view-device/<device_id>/")
def view_device(device_id):
    checks = health_check_service.get_previous_checks(device_id)
    device = devices_service.get_single_device(device_id)
    available_checks = health_check_service.get_all_health_checks()
    return render_template('view-device.html', checks=checks, device=device, available_checks=available_checks)


@device_blueprint.route('/list-devices')
def list_devices():
    devices = get_all_devices()
    return render_template('list-devices.html', devices=devices)


@device_blueprint.route("/run-all-single-device-checks/<device_id>")
def run_all_single_device_checks(device_id):
    health_check_service.run_all_health_checks_for_single_device(device_id)
    return render_template("run-all-single-device-checks.html")

