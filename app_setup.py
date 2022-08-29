# The run file is where we have the code instructions to run our flask application.

from datetime import datetime
import sched
from flask import Flask
from flask_migrate import Migrate
from fortinet_healthcheck import blueprints
from fortinet_healthcheck.services import health_check_service
from fortinet_healthcheck.services import devices_service 
from extensions import db
from dotenv import load_dotenv
import os
from flask_apscheduler import APScheduler
from apscheduler.triggers.interval import IntervalTrigger

load_dotenv()

db_user = os.getenv('POSTGRES_USER')
db_name = os.getenv('POSTGRES_DB')
db_password = os.getenv('POSTGRES_PASSWORD')
db_host = os.getenv('POSTGRES_HOST')
scheduler = APScheduler()

class Config:
    REDIS_URL = "redis://redis:6379/0"
    QUEUES = "default"
    SCHEDULER_API_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"



def example():
    with open("mine.txt", "a") as f:
        f.write(f"{datetime.now()}\n")

def create_app():
    # Create an app variable and initialize Flask
    app = Flask(__name__, template_folder='fortinet_healthcheck/templates',
                static_folder='fortinet_healthcheck/static',
                static_url_path='/static/')
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate = Migrate(app, db, compare_type=True)
    migrate.init_app(app, db)

    scheduler.init_app(app)
    
    @scheduler.task(IntervalTrigger(seconds=3600), id='do_run_all_healthchecks')
    def run_healthchecks_scheduler():
        for device in devices_service.get_all_devices():
            health_check_service.run_all_health_checks_for_single_device(device.id)
    
    scheduler.start()


    # Get configuration from environment variables
    

    # REGISTER BLUEPRINTS
    for blueprint in blueprints.BLUEPRINTS:
        app.register_blueprint(blueprint)
    return app


