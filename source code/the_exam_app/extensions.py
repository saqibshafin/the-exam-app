# this file includes all the extensions I will use with Flask


from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Will be used to instantiate the database and the login manager when called from __init__.py
login_manager = LoginManager()
db = SQLAlchemy()