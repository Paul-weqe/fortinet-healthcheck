from flask import Blueprint, render_template
from fortinet_healthcheck.services import devices_service

# Initialize an object of a blueprint and pass in the blueprint name 
# for this specific component which in our case is ‘auth_blueprint’

auth_blueprint = Blueprint('auth_blueprint', __name__)

# Creating REST API. Use the route decorator to tell Flask which URL 
# should be handled by the home_page() function

@auth_blueprint.route("/")
def home_page():
    devices = devices_service.get_all_devices()
    return render_template("index.html", devices=devices)

