from fortinet_healthcheck.models import Vendor

def get_all_vendors():
    return Vendor.query.all()

# Used for the vendor dropdown while creating/editting 
# a device 
def get_vendor_choices():
    vendors = get_all_vendors()
    for v in vendors:
        yield (v.id, v.vendor_name) 
