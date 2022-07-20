from .auth import auth_blueprint
from .devices import device_blueprint
from .health_checks import health_check_blueprint

BLUEPRINTS = [
    auth_blueprint,
    device_blueprint,
    health_check_blueprint
]
