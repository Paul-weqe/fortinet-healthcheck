from flask import Blueprint, render_template, flash, url_for, redirect
from fortinet_healthcheck.services import health_check_service, devices_service
from fortinet_healthcheck.forms import CreateHealthCheckForm
health_check_blueprint = Blueprint('health_check_blueprint', __name__)


def parse_check_in_output(output: str) -> list:
    output_list = []
    for x in output.split("\n"):
        if x.strip() == "":
            pass
        output_list.append(x.strip())
    return output_list


@health_check_blueprint.route("/create-health-check", methods=['GET', 'POST'])
def create_health_check_view():
    form = CreateHealthCheckForm()

    if form.validate_on_submit():
        outputs_list = parse_check_in_output(form.check_result.data)
        health_check = health_check_service.create_health_check(
            name=form.name.data, command=form.command.data, check_type=form.check_type.data,
            description=form.description.data, check_outputs=outputs_list
        )
        flash('success', f'successfully created health check {health_check.name}')
        return redirect(url_for('auth_blueprint.home_page'))
    return render_template('create-health-check.html', form=form)


@health_check_blueprint.route('/view-health-checks', methods=['GET', 'POST'])
def view_health_checks():
    form = CreateHealthCheckForm()
    check_groups = health_check_service.get_all_health_check_groups()

    if form.validate_on_submit():
        outputs_list = parse_check_in_output(form.check_result.data)
        health_check = health_check_service.create_health_check(
            name=form.name.data, command=form.command.data, check_type=form.check_type.data,
            description=form.description.data, check_outputs=outputs_list
        )
        flash('success', f'successfully created health check {health_check.name}')
        return redirect(url_for('auth_blueprint.home_page'))
    return render_template('view-health-checks.html', form=form, check_groups=check_groups)


@health_check_blueprint.route('/run-device-health-check/<device_id>')
def run_device_health_check(device_id):
    result = health_check_service.run_all_health_checks_for_single_device(device_id)
    return redirect(url_for('devices_blueprint.view_device', device_id=device_id))


@health_check_blueprint.route('/run-all-health-checks')
def run_all_health_checks():
    devices = devices_service.get_all_devices()

    for device in devices:
        health_check_service.run_all_health_checks_for_single_device(device.id)

    result = health_check_service.run_all_health_checks_for_single_device()
    return redirect(url_for('health_check_blueprint.view_health_checks'))