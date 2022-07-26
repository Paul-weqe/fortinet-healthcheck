from datetime import datetime

from .connection_service.base_healthcheck import BaseHealthCheck
from .connection_service.netmiko_conn import create_connection
from fortinet_healthcheck.models import HealthCheck, Device, Check, HealthCheckOutput, CheckGroup
from extensions import db


def create_health_check(name: str, command: str, check_type: str, description: str = "", check_outputs: list = []):
    allowed_check_types = [
        "or", "and", "not"
    ]

    if check_type not in allowed_check_types:
        raise Exception(f"Error, '{check_type}' is not part of the required check types")

    health_check = HealthCheck(
        name=name, command=command, check_type=check_type, description=description
    )
    db.session.add(health_check)
    db.session.commit()

    for output in check_outputs:
        create_health_check_output(health_check.id, output)

    return health_check


def create_health_check_output(health_check_id: int, expected_output) -> HealthCheckOutput:
    health_check_output = HealthCheckOutput(
        health_check_id=health_check_id, expected_output=expected_output
    )
    db.session.add(health_check_output)
    db.session.commit()
    return health_check_output


def get_health_check_expected_outputs(health_check: HealthCheck):
    expected_outputs = []
    for x in health_check.check_outputs:
        expected_outputs.append(x.expected_output)
    return expected_outputs


def run_all_health_checks_for_single_device(device_id: int):
    if HealthCheck.query.count() == 0:
        return {str(device_id): {}, 'group_id': None}
    query_ids = list(HealthCheck.query.with_entities(HealthCheck.id).all())
    health_checks_ids = []
    for entry in query_ids:
        health_checks_ids.append(entry[0])
    return run_multiple_health_checks(device_id, health_checks_ids)


def run_multiple_health_checks(device_id: int, health_check_ids: list):
    check_group = CheckGroup(device_id=device_id)
    db.session.add(check_group)
    db.session.commit()

    device = Device.query.get(device_id)
    conn = create_connection(hostname=device.hostname, username=device.username, password=device.encoded_password)
    result = {str(device_id): {}, 'group_id': check_group.id}

    for hc_id in health_check_ids:
        health_check = HealthCheck.query.get(hc_id)
        expected_outputs = get_health_check_expected_outputs(health_check)
        base_health_check = BaseHealthCheck(conn)
        output = base_health_check.run_single_command(health_check.command)
        hc_result = base_health_check.check_result(
            output, expected_outputs, health_check.check_type
        )
        result[str(device_id)][hc_id] = hc_result
        time_completed = datetime.now()
        device.last_healthcheck = time_completed
        check = Check(
            device_id=device_id, health_check_id=hc_id, is_successful=hc_result, timestamp=time_completed,
            check_group_id = check_group.id
        )
        db.session.add(check)
        db.session.commit()

    conn.disconnect()
    return result


def get_previous_checks(device_id: int):
    device = Device.query.get(device_id)
    checks = device.checks
    return checks


def run_check(device_id: int, health_check_id: int):
    device = Device.query.get(device_id)
    health_check = HealthCheck.query.get(health_check_id)
    expected_outputs = []
    for c in health_check.check_outputs:
        expected_outputs.append(c.expected_output)

    conn = create_connection(
        hostname=device.hostname, username=device.username, password=device.encoded_password
    )
    base_health_check = BaseHealthCheck(conn)
    conn.disconnect()


def get_all_health_checks():
    health_checks = HealthCheck.query.all()
    return health_checks


def get_all_health_check_groups():
    return CheckGroup.query.all()
