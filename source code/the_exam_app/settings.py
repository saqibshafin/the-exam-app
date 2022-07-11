# This settins.py file is the config file for our application.
# When I use 'flask run', it's going to automatically put everything from the
# .env file to the 'environment', and so this settings file will get those
# things from the environment


import os  # So that I can get environment variables from the .env file

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    # SQLALCHEMY_DATABASE_URI = sqlite:///dbx.sqlite3  # '///' 3 slashesh indicate 
    # relative path for the database
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False  # [1]


"""
Links/notes
[1] How do I know if I can disable SQLALCHEMY_TRACK_MODIFICATIONS?
        https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications
"""