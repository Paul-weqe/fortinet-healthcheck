# SQLAlchemy is a library that facilitates the communication between 
# Python programs and databases. Most of the times, this library is used
# as an Object Relational Mapper (ORM) tool that translates Python classes
# to tables on relational databases and automatically converts function 
# calls to SQL statements.

# Flask-SQLAlchemy is an extension for Flask that adds support for SQLAlchemy
#  to your application. It aims to simplify using SQLAlchemy with Flask by 
# providing useful defaults and extra helpers that make it easier to accomplish 
# common tasks.
from flask_sqlalchemy import SQLAlchemy

# Creating an instance of the SQLAlchemy object
db = SQLAlchemy()

# Context Manager for the db sessions
# To always ensure they open and close whatever the user accesses
# a database session. 
class DbSessionContext(object):
    def __init__(self):
        self.db = db

    def __enter__(self):
        return self.db.session

    def __exit__(self, type, value, traceback):
        self.db.session.close()
