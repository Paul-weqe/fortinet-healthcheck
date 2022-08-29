from datetime import datetime

from .connection_service.base_healthcheck import BaseHealthCheck
from .connection_service.netmiko_conn import create_connection
from fortinet_healthcheck.models import HealthCheck, Device, Check, HealthCheckOutput, CheckGroup
from fortinet_healthcheck.helpers import *


def create_health_check(name: str, command: str, check_type: str, description: str = "", check_outputs=None, vendor_id=None):
    if check_outputs is None:
        check_outputs = []
    allowed_check_types = [
        "or", "and", "not"
    ]
    if check_type not in allowed_check_types:
        raise Exception(f"Error, '{check_type}' is not part of the required check types")

    health_check = HealthCheck(
        name=name, command=command, check_type=check_type, description=description
    )
    health_check.vendor_id = int(vendor_id) if vendor_id is not None else None
    insert_into_db(health_check)
    for output in check_outputs:
        create_health_check_output(health_check.id, output)
    
    return health_check


def edit_healthcheck(
        health_check_id: int, name: str, command: str, check_type: str, description: str="", check_outputs=None, vendor_id=None
    ):
    health_check = HealthCheck.query.get(health_check_id)
    health_check.name = name
    health_check.command = command 
    health_check.check_type = check_type
    health_check.description = description
    if check_outputs is not None:
        for output in health_check.check_outputs:
            delete_from_db(output)
        for output in check_outputs:
            create_health_check_output(health_check.id, output)
    commit_changes()
    return health_check


def delete_healthcheck(healthcheck_id):
    healthcheck = HealthCheck.query.get(healthcheck_id)
    checks = healthcheck.checks
    check_groups = []
    for check in checks:
        check_groups.append(check.check_group)
    
    check_groups = list(set(check_groups))
    
    delete_from_db(healthcheck)
    for group in check_groups:
        if group.checks == 0:
            delete_from_db(group)
    
    return True

# For each of the checks, we need one/more outputs that we can check against.
# Here, we insert each of those outputs
def create_health_check_output(health_check_id: int, expected_output) -> HealthCheckOutput:
    health_check_output = HealthCheckOutput(
        health_check_id=health_check_id, expected_output=expected_output
    )
    insert_into_db(health_check_output)
    
    return health_check_output

# Each healthcheck has got what it expects in order to be considered a 
# success, here we collect that information for a single healthcheck. 
def get_health_check_expected_outputs(health_check: HealthCheck):
    expected_outputs = []
    for x in health_check.check_outputs:
        expected_outputs.append(x.expected_output)
    return expected_outputs


def run_checks_for_healthcheck(healthcheck_id: int):
    with DbSessionContext() as session:
        health_checks = session.query(
            HealthCheck, Device
        ).filter(
            HealthCheck.vendor_id == Device.vendor_id
        ).filter(
            HealthCheck.id == healthcheck_id 
        ).all()

        for h_c in health_checks:
            run_multiple_health_checks(h_c[1].id, [h_c[0].id])



def run_all_health_checks_for_single_device(device_id: int):    
    health_checks_ids = []
    # fetch all the healthchecks for the specific device
    # associated with the device(it's vendor's healthchecks). 
    with DbSessionContext() as session:
        health_checks = session.query(
                HealthCheck, Device
            ).filter(
                HealthCheck.vendor_id == Device.vendor_id
            ).filter(
                Device.id == device_id
            ).all()
        
        for health_check in health_checks:
            health_checks_ids.append(health_check[0].id)
    
    return run_multiple_health_checks(device_id, health_checks_ids)


# Runs multiple Healthchecks for a single device.
# E.g, for device 198.168.0.1(id=1), if we want to run a healthcheck called "interface HC"(id=1) 
# and "Security HC"(id=2), we will get the if for these healthchecks
# and call run_multiple_health_checks(3, [1, 2]). 
def run_multiple_health_checks(device_id: int, health_check_ids: list):
    check_group = CheckGroup(device_id=device_id)
    insert_into_db(check_group)
    
    device = Device.query.get(device_id)
    conn = create_connection(hostname=device.hostname, username=device.username, password=device.encoded_password)
    result = {str(device_id): {}, 'group_id': check_group.id}

    for hc_id in health_check_ids:
        health_check = HealthCheck.query.get(hc_id)
        expected_outputs = get_health_check_expected_outputs(health_check)

        # Creating an instance of the BaseHealthCheck class
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
        insert_into_db(check)

    conn.disconnect()
    return result

# show all health checks associated to a specific device
def get_all_device_health_checks(device_id):
    vendor = Device.query.get(device_id).vendor
    return  vendor.health_checks


def get_previous_checks(device_id: int):
    device = Device.query.get(device_id)
    return device.checks


def get_all_health_checks():
    health_checks = HealthCheck.query.all()
    return health_checks


def get_all_health_check_groups():
    return CheckGroup.query.all()
