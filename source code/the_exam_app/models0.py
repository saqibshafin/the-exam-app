from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbxx.sqlite3'
db = SQLAlchemy(app)

class User(db.Model):
    #__tablename__ = 'user'
# Some parts that are required in SQLAlchemy are optional in Flask-SQLAlchemy. 
# For instance the table name is automatically set for you unless overridden. 
# It’s derived from the class name converted to lowercase and with “CamelCase” 
# converted to “camel_case”. To override the table name, set the __tablename__ 
# class attribute.    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(100))  # will be stored as hash
    admin = db.Column(db.Boolean)
    teacher = db.Column(db.Boolean)
# if neither of the above two(admin/teacher) is true for a user, he will be considered a student
    #classes = db.Column(db.Integer)  # Indicates which classes a teacher teaches

subs_of_a_class = db.Table('subs_of_a_class', 
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'), primary_key=True)
)

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(25))
    #section = db.Column(db.String(10))  # section a,b,c...

    subjects = db.relationship('Subject', secondary=subs_of_a_class, lazy=True, 
        backref='which_class')

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(50))
    #classs_id = db.Column(db.Integer, db.ForeignKey('classs.id'),
    #    nullable = False)

#class ClasssDetailed(db.Model):  # table name becomes 'class_detailed'
#    classs_id = db.Column(db.Integer, db.ForeignKey('classs.id'),
#        nullable = False)
#    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'),
#        nullable = False)

#class Subject_detailed(db.Model):

"""class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String(50))
    classs_id = db.Column(db.Integer, db.ForeignKey('classs.id'),
        nullable = False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'),
        nullable = False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'),
        nullable = False)
    question = db.Column(db.Text)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'),
        nullable = False)
    answer = db.Column(db.Text)
"""