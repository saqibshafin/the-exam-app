import click # 'click' is the library that Flask uses whenever I run 'Flask run'
from flask.cli import with_appcontext # This with_appcontext decorator makes sure that any 
# command we run uses the configuration of the app. If I din't use it, any command given would
# run alone without activating the Flass app first. And because the command/app deals with the
# database, we have to know what the database configuration is.
from .extensions import db
#from .models0 import Class, Subject, subs_of_a_class
#from .models import Class, Subject, Classsub  #, subs_of_a_class
from .models import User, Question, Answer  # Importing the models helps the tables get created,
    # even though we are not directly using them

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()