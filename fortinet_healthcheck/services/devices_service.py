from fortinet_healthcheck.models import Device
from extensions import db


def create_device(alias: str, hostname: str, username: str, port: int, password: str):
    device = Device(
        alias=alias, username=username, hostname=hostname, port=port, encoded_password=password
    )
    db.session.add(device)
    db.session.commit()
    return device


def get_all_devices():
    devices = Device.query.all()
    return devices


def get_single_device(id: int) -> Device:
    return Device.query.get(id)
