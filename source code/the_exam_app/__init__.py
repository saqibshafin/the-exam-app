from flask import Flask

from .extensions import db, login_manager
from .commands import create_tables
from .routes.main import main
from .routes.auth import auth
from .models import User

"""app = Flask(__name__)
app.config.from_pyfile('settings.py')  # goes to settings.py for config
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)"""

def create_app(config_file='settings.py'):
    app = Flask(__name__)  # this line sets the name of this Flask app as 'app'.
    app.config.from_pyfile(config_file)  # goes to settings.py for config
    app.config['SQLALCHEMY_ECHO'] = True

    # Instantiating db and login_manager
    db.init_app(app) # 'app' is an object passed in to 'init_app' to instantiate it. It does what 
        # 'db = SQLAlchemy(app)' does. **Why didn't I just do it in the extensions.py file??
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)  # 'User' is a table here

    app.cli.add_command(create_tables)

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app 

"""from "the question_answer app" import app, db
from app.models import User

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}"""


"""
Links/notes
[1]
[2] 
"""