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
