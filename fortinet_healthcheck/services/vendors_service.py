from fortinet_healthcheck.models import Vendor
from fortinet_healthcheck.helpers import *

def get_all_vendors():
    return Vendor.query.all()

# Used for the vendor dropdown while creating/editting 
# a device 
def get_vendor_choices():
    vendors = get_all_vendors()
    for v in vendors:
        yield (v.id, v.vendor_name) 


def create_vendor(vendor_name: str, netmiko_alias: str):
    vendor_exists = Vendor.query.filter_by(vendor_name=vendor_name).first() is not None

    if vendor_exists:
        raise Exception(f"Vendor {vendor_exists} already exists")
    vendor = Vendor(vendor_name = vendor_name, netmiko_alias=netmiko_alias)
    insert_into_db(vendor)
    return vendor