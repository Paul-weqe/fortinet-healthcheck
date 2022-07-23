from flask import Flask
from flask_migrate import Migrate
from fortinet_healthcheck import blueprints
from extensions import db
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, template_folder='fortinet_healthcheck/templates',
            static_folder='fortinet_healthcheck/static',
            static_url_path='/cdn/')

db.init_app(app)
migrate = Migrate(app, db)


DB_USER = os.getenv('POSTGRES_USER')
DB_NAME = os.getenv('POSTGRES_DB')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('POSTGRES_HOST')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

# REGISTER BLUEPRINTS
for blueprint in blueprints.BLUEPRINTS:
    app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run(debug=True)
