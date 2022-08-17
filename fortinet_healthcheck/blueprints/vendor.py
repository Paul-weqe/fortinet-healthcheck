from flask import Blueprint, render_template, redirect, url_for, flash
from fortinet_healthcheck.forms import CreateVendorForm
from fortinet_healthcheck.services import vendors_service

vendor_blueprint = Blueprint('vendor_blueprint', __name__)


@vendor_blueprint.route('/view-vendors')
def list_vendors_view():
    all_vendors = vendors_service.get_all_vendors()
    return render_template('view-vendors.html', all_vendors=all_vendors)

@vendor_blueprint.route("/create-vendor", methods=['GET', 'POST'])
def create_vendor_view():
    form = CreateVendorForm()
    all_vendors = vendors_service.get_all_vendors()
    
    if form.validate_on_submit():
        vendor_name = form.vendor_name.data
        netmiko_alias = form.netmiko_alias.data
        vendors_service.create_vendor(
            vendor_name = vendor_name,
            netmiko_alias = netmiko_alias
        )
        flash("success", f"Successfully added vendor {vendor_name}")
        return redirect(url_for("vendor_blueprint.list_vendors_view"))

    return render_template('create-vendor.html', form=form, all_vendors=all_vendors)
