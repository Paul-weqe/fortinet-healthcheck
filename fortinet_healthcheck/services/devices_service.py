from fortinet_healthcheck.models import Device
from extensions import DbSessionContext

# invoke the database object, create entries, and insert them into the database
# table. Keep in mind that anything we add to the session needs to be committed to the
# database in order to be permanent:
def create_device(alias: str, hostname: str, username: str, port: int, password: str, vendor_id=None):
    device = Device(
        alias=alias, username=username, hostname=hostname, port=port, encoded_password=password
    )
    device.vendor_id = int(vendor_id) if vendor_id is not None else None
    
    with DbSessionContext() as session:
        session.add(device)
        session.commit()
        session.close()
    
    return device


def get_all_devices():
    devices = Device.query.all()
    return devices


def get_single_device(id: int) -> Device:
    return Device.query.get(id)
