from .auth import auth_blueprint
from .devices import device_blueprint
from .health_checks import health_check_blueprint

# Blueprints aid in organizing components of our web applications into distinct components

BLUEPRINTS = [
    auth_blueprint,
    device_blueprint,
    health_check_blueprint
]
