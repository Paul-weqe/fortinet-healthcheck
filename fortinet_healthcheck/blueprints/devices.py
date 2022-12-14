from flask import Blueprint, render_template, flash, url_for, redirect
from fortinet_healthcheck.forms import CreateDeviceForm
from fortinet_healthcheck.services import health_check_service, devices_service
from fortinet_healthcheck.services.devices_service import get_all_devices
from fortinet_healthcheck.services import vendors_service

# Initialize an object of a blueprint and pass in the blueprint name 
# for this specific component which in our case is ‘device_blueprint’
device_blueprint = Blueprint('devices_blueprint', __name__)


# Creating REST API. Use the route decorator to tell Flask which URL
# should be handled by the create_device() function
@device_blueprint.route("/create-device", methods=['GET', 'POST'])
@device_blueprint.route("/update-device/<device_id>", methods=['GET', 'POST'])
def create_device(device_id=None):
    VENDOR_CHOICES = list(vendors_service.get_vendor_choices())
    device = None
    if device_id is not None:
        device = devices_service.get_single_device(device_id)

    form = CreateDeviceForm()
    if device is not None:
        form = CreateDeviceForm(
            alias=device.alias, hostname=device.hostname, username=device.username, 
            vendor=device.vendor_id, port=device.port
        )
    form.vendor.choices = VENDOR_CHOICES

    if form.validate_on_submit():
        if device_id is None:
            dev = devices_service.create_device(
                alias=form.alias.data, hostname=form.hostname.data, username=form.username.data,
                port=form.port.data, password=form.password.data, vendor_id=form.vendor.data
            )
            flash('success', f"Successfully added device {dev.hostname}")
        else:
            dev = devices_service.update_device(
                device_id=device_id, alias=form.alias.data, hostname=form.hostname.data, username=form.username.data,
                port=form.port.data, password=form.password.data, vendor_id=form.vendor.data
            )
            flash('success', f"Successfully updated device {dev.hostname}")
        
        return redirect(url_for('auth_blueprint.home_page'))
    return render_template('create-device.html', form=form, device_id=device_id)


@device_blueprint.route("/view-device/<device_id>/")
def view_device(device_id):
    checks = health_check_service.get_previous_checks(device_id)
    device = devices_service.get_single_device(device_id)
    available_checks = health_check_service.get_all_device_health_checks(device_id)
    return render_template('view-device.html', checks=checks, device=device, available_checks=available_checks)


@device_blueprint.route("/delete-device/<device_id>")
def delete_device_view(device_id):
    alias = devices_service.delete_single_device(device_id)
    flash('danger', f"Device '{alias}' has been deleted")
    return redirect(url_for('devices_blueprint.list_devices'))


@device_blueprint.route('/list-devices')
def list_devices():
    devices = get_all_devices()
    return render_template('list-devices.html', devices=devices)


@device_blueprint.route("/run-all-single-device-checks/<device_id>")
def run_all_single_device_checks(device_id):
    health_check_service.run_all_health_checks_for_single_device(device_id)
    return render_template("run-all-single-device-checks.html")


@device_blueprint.route("/single-hc-single-device/<device_id>/<healthcheck_id>")
def run_single_healthcheck_for_single_device(device_id, healthcheck_id):
    return render_template("single-healthcheck-single-device.html")


