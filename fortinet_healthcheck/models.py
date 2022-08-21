# Models is for database stuff

from extensions import db
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

# Defining the User object/class
# User inherits all the characteristics and variables related to db.Model
class User(db.Model):

    __tablename__ = "users"

    # primary_key=True defines the id column as a primary key, which will assign 
    # it a unique value by the database for each entry
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    
    confirmation_sent = db.Column(db.Boolean, default=False)
    confirmed_at = db.Column(db.DateTime, nullable=True)
    confirmation_token = db.Column(db.String, unique=True)
    is_confirmed = db.Column(db.Boolean, default=False)

    # The __repr__ method returns the string representation of an object. 
    # Typically, the __repr__() returns a string that can be executed and 
    # ield the same value as the object.
    def __repr__(self):
        return f"<User {self.username}>"


# Assume device is a FortiGate
# create a devices database object and its associated primary key and various columns
# This is the database model object
# We declare a database model object with id as the primary key and string fields for
# alias, hostname, username, and encoded_password
class Device(db.Model):

    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alias = db.Column(db.String)
    hostname = db.Column(db.String)
    #vendor = db.Column(db.String(40))
    username = db.Column(db.String)
    port = db.Column(db.Integer)
    encoded_password = db.Column(db.String(100))
    last_healthcheck = db.Column(db.DateTime, nullable=True)

    checks = db.relationship('Check', backref='device', lazy=True, order_by='Check.timestamp.desc()')
    check_groups = db.relationship('CheckGroup', backref='device', lazy=True, order_by='CheckGroup.timestamp.desc()')

    def __repr__(self):
        return f"<Device {self.hostname}>"


"""
 RUN
 
 Each time a healthcheck is run on a device, a number of checks are executed. 
 e.g we can have 5 checks (one for interface, one for uptime etc...)
 
 Each time we have a run of the healthchecks, we create a checkgroup that contains
 the checks that have been run and their output. If successful or not. 
 
 We therefore have each of the checks being contained in a checkgroup 
 and each device has multiple check groups. Later on we can see what the output for each 
 of the different healthchecks were depeinding on when it was run. 
 
"""
class CheckGroup(db.Model):

    __tablename__ = "check_groups"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, server_default=func.now())
    checks = db.relationship('Check', backref='check_group', lazy=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=True)

    @hybrid_property
    def successful_checks(self):
        count = 0
        for check in self.checks:
            if check.is_successful:
                count += 1
        return count

    @hybrid_property
    def failed_checks(self):
        return len(self.checks) - self.successful_checks

    @hybrid_property
    def percentage_success(self):
        total_checks = len(self.checks)
        return (self.successful_checks / total_checks) * 100

    def __str__(self):
        return f"<CheckGroupId: {self.id}>"


class HealthCheck(db.Model):

    __tablename__ = "health_checks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    command = db.Column(db.String(300), unique=True)

    # check type ('and', 'or' and 'not')
    check_type = db.Column(db.String(10))
    description = db.Column(db.Text, default="")

    # FKs
    check_outputs = db.relationship('HealthCheckOutput', backref='health_check', lazy=True)
    checks = db.relationship('Check', backref='health_check', lazy=True)

    @hybrid_property
    def checks_count(self):
        return len(self.checks)

    def __repr__(self):
        return f"<[HealthCheck: {self.name}] [Command: {self.command}]>"


class HealthCheckOutput(db.Model):

    __tablename__ = "health_check_outputs"

    id = db.Column(db.Integer, primary_key=True)
    health_check_id = db.Column(db.Integer, db.ForeignKey('health_checks.id'), nullable=False)
    expected_output = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<HealthCheck Output: [{self.expected_output}]>"




class Check(db.Model):

    __tablename__ = "checks"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, server_default=func.now())
    is_successful = db.Column(db.Boolean, nullable=True)

    # FOREIGN KEY
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    health_check_id = db.Column(db.Integer, db.ForeignKey('health_checks.id'), nullable=False)
    check_group_id = db.Column(db.Integer, db.ForeignKey('check_groups.id'), nullable=False)

    def __repr__(self):
        return f"<Check Time: {self.timestamp} Device: {self.device_id} HealthCheck: {self.health_check_id}>"

    @hybrid_property
    def time_since(self):
        td = datetime.now() - self.timestamp
        return {
            'timedelta': td,
            'days': td.days,
            'hours': td.seconds // 3600,
            'minutes': (td.seconds // 60) % 60
        }

    @hybrid_property
    def time_since_str(self):
        result = ""
        ts = self.time_since
        if ts['days'] == 1:
            result += f"{ts['days']} day, "
        else:
            result += f"{ts['days']} days, "

        if ts['hours'] == 1:
            result += f"{ts['hours']} hour, "
        else:
            result += f"{ts['hours']} hours, "

        if ts['minutes'] == 1:
            result += f"{ts['minutes']} min"
        else:
            result += f"{ts['minutes']} mins"

        return result
