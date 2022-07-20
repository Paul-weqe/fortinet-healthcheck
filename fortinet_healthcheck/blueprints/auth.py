from flask import Blueprint, render_template
from fortinet_healthcheck.services import devices_service

auth_blueprint = Blueprint('auth_blueprint', __name__)


@auth_blueprint.route("/")
def home_page():
    devices = devices_service.get_all_devices()
    return render_template("index.html", devices=devices)

