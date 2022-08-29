from dataclasses import dataclass
from fortinet_healthcheck.models import Device
from fortinet_healthcheck.helpers import delete_from_db, insert_into_db, DbSessionContext, delete_from_db

# invoke the database object, create entries, and insert them into the database
# table. Keep in mind that anything we add to the session needs to be committed to the
# database in order to be permanent:
def create_device(alias: str, hostname: str, username: str, port: int, password: str, vendor_id=None):
    device = Device(
        alias=alias, username=username, hostname=hostname, port=port, encoded_password=password
    )
    device.vendor_id = int(vendor_id) if vendor_id is not None else None
    insert_into_db(device)
    return device

def update_device(device_id: int, alias: str, hostname: str, username: str, port: int, password: str = None, vendor_id: int = None):
    
    
    device = Device.query.get(device_id)
    device.alias = alias
    device.hostname = hostname
    device.username = username
    device.port = port
    if password is not None or password.strip() != "":
        device.encoded_password = password
    if vendor_id is not None:
        device.vendor_id = vendor_id
    
    with DbSessionContext() as session:
        session.commit()
    return device


def get_all_devices():
    devices = Device.query.all()
    return devices


def get_single_device(id: int) -> Device:
    return Device.query.get(id)

def delete_single_device(device_id: int):
    device = Device.query.get(device_id)
    alias = device.alias
    delete_from_db(device)
    return alias