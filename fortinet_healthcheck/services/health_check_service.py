from datetime import datetime

from .connection_service.base_healthcheck import BaseHealthCheck
from .connection_service.netmiko_conn import create_connection
from fortinet_healthcheck.models import HealthCheck, Device, Check
from extensions import db


def create_health_check(name: str, command: str, check_type: str, description: str = ""):
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
    return health_check


def get_health_check_expected_outputs(health_check: HealthCheck):
    expected_outputs = []
    for x in health_check.check_outputs:
        expected_outputs.append(x.expected_output)
    return expected_outputs


def run_multiple_health_checks(device_id: int, health_check_ids: list):
    device = Device.query.get(device_id)
    conn = create_connection(hostname=device.hostname, username=device.username, password=device.encoded_password)
    result = {}

    for hc_id in health_check_ids:
        health_check = HealthCheck.query.get(hc_id)
        expected_outputs = get_health_check_expected_outputs(health_check)
        base_health_check = BaseHealthCheck(conn)
        output = base_health_check.run_single_command(health_check.command)
        hc_result = base_health_check.check_result(
            output, expected_outputs, health_check.check_type
        )
        time_completed = datetime.now()
        device.last_healthcheck = time_completed
        check = Check(device_id=device_id, health_check_id=hc_id, is_successful=hc_result, timestamp=time_completed)
        db.session.add(check)
        db.session.commit()


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


