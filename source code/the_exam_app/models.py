# in this file we will create the models that are necessary for this app


from enum import unique
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from .extensions import db  # so that I can create the tables

"""class User(db.Model):
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
    # classes = db.Column(db.Integer)  # Indicates which classes a teacher teaches"""

"""exams_ofa_class_sub = db.Table('exams_ofa_class',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('class_sub_id', db.Integer, db.ForeignKey('subs_of_a_class.id'), primary_key=True),
    db.Column('exam_id', db.Integer, db.ForeignKey('exam.id'), primary_key=True)
)"""

"""subs_of_a_class = db.Table('subs_of_a_class', 
    #db.Column('id', db.Integer, primary_key=True),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'), primary_key=True),

    #db.Column('exams', db.relationship('Exam', secondary=exams_ofa_class_sub, lazy=True,
    #    backref='examofany_class_sub'))
)

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(25))
    #section = db.Column(db.String(10))  # section a,b,c...

    subjects = db.relationship('Subject', secondary=subs_of_a_class, lazy=True, 
        backref='which_class')  # Why did I use backref here? Is it necessary?
# https://docs.sqlalchemy.org/en/14/orm/relationship_api.html#sqlalchemy.orm.relationship.params.backref        

class Subject(db.Model):  # Beware of this table having bidirectional relationship
# with Class or not.
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(50))
    #classs_id = db.Column(db.Integer, db.ForeignKey('classs.id'),
    #    nullable = False)"""

"""class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String(50))"""
    
"""classs_id = db.Column(db.Integer, db.ForeignKey('classs.id'),
        nullable = False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'),
        nullable = False)"""

"""class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(25))
    #section = db.Column(db.String(10))  # section a,b,c...
    subjects = db.relationship('Subject', secondary='Classsub',backref='classes')

class Subject(db.Model):  # Beware of this table having bidirectional relationship
# with Class or not.
    id = db.Column(db.Integer, primary_key=True)
    sub_name = db.Column(db.String(50))

class Classsub(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), primary_key=True)

    #sub = db.relationship('Subject', backref=db.backref('classes'))
    sub = db.relationship('Subject', backref=db.backref('classsub', passive_deletes='all'))  #cascade='all,delete'))
    #clss = db.relationship('Class', backref=db.backref('subjects'))
    clss = db.relationship('Class', backref=db.backref('classsub', passive_deletes='all'))

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ques_name = db.Column(db.String(50))
    question = db.Column(db.Text)
    
    classsub = db.relationship('Ques_classsub', backref=db.backref('question'))

class Ques_classsub(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    classsub_id = db.Column(db.Integer, db.ForeignKey('classsub.id'), primary_key=True)
    ques_id =  db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)

    classsub = db.relationship('Classsub', backref=db.backref('question'))
    ques = db.relationship('Question', backref=db.backref('classsub'))"""

"""class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'),
    #    nullable = False)
    ques_name = db.Column(db.String(50))
    question = db.Column(db.Text)"""



"""students_of_teacher = db.Table('students_of_teacher',
    db.Column('teacher_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)"""

class User(UserMixin, db.Model):
    #__tablename__ = 'user'
    # Some parts that are required in SQLAlchemy are optional in Flask-SQLAlchemy. 
    # For instance the table name is automatically set for you unless overridden. 
    # It’s derived from the class name converted to lowercase and with “CamelCase” 
    # converted to “camel_case”. To override the table name, set the __tablename__ 
    # class attribute.    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)  # will be stored as hash
    #admin = db.Column(db.Boolean)
    teacher = db.Column(db.Boolean)
    student = db.Column(db.Boolean)  # Removed 'admin' field to speed up the sql queries.
    # If neither of the above two(admin/teacher) is true for a user, he will be considered a student
    # classes = db.Column(db.Integer)  # Indicates which classes a teacher teaches
    current_class = db.Column(db.String(20))
    
    subject = db.relationship('Subject', backref='user')  # One(User) to many(Subject) relationship
    # with the table Question
    # question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    #question = db.relationship('Question', backref='user')  # One(User) to many(Question) relationship
    # with the table Question
    # **Where is the lazy=True statement??
    answer = db.relationship('Answer', backref='user')# One(User) to many relationship with
    # the table Answer

    #students_of_teacher = db.relationship('User', secondary=students_of_teacher, lazy='subquery',
    #    backref=db.backref('teachers', lazy=True))

    @property
    def unhashed_password(self):  #**what is self doing here?
        raise AttributeError('Cannot view unhashed password!')

    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)
    # [1] What happens is, when we create a user, we start with the unhashed password and set it,
    # and this will automatically take that unhashed password and generate a password hash
    # and set it to 'password'(self.password). And then we will save(in the db) this hashed
    # version of the original password instead of the original password the user typed in.

class Students_of_teacher(db.Model):  # [1]
    # Also, this table has composite primary keys.
    
    #__tablename__ = 'stakeholder'
    #id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    subject_id = db.Column(db.ForeignKey('subject.id'), nullable=False, primary_key=True)  # db.Integer
        # intentionally not used here.
    
    students_of_teacher = db.relationship("User", foreign_keys=[student_id])  # [1]
        # note that 'student_id' is in list form '[1]'
    teacher = db.relationship("User", foreign_keys=[teacher_id])
    subject = db.relationship("Subject", foreign_keys=[subject_id])

    question_access_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship('Question', foreign_keys=[question_access_id])
    #    backref='students_with_access')

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    classs = db.Column(db.String(20))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    question = db.relationship('Question', backref='subject')

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))  # should it be "question.name"
        # or "exam.type"? In the future, change the "Exam Type" button
        # into a dropdown list.
    question = db.Column(db.Text)

    #classs = db.Column(db.String(15))
    #subj = db.Column(db.String(20))

    #user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    #user = db.relationship('User', backref='questions')
    #user_id = db.Column(db.ForeignKey('students_of_teacher.id'))
    
    subject_id = db.Column(db.Integer,db.ForeignKey('subject.id'))#, unique=True)
    
    examstart_datetime = db.Column(db.String(50))
    examend_datetime = db.Column(db.String(50))

    total_marks = db.Column(db.Integer)

    answer = db.relationship('Answer', backref='question')# One(Question) to many(Answer) relationship
    # with the table Answer

class Answer(db.Model):  # [2] we could also create the Answer table with a composite 
    # key which is made of user.id and question.id, and these two elements make up the 
    # primary key in the Answer table. This would also be called a compound key because 
    # both elements of the composite key are foreign keys themselves in this table.
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text)

    marks_attained = db.Column(db.Integer)

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'),
        nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #user = db.relationship('User', backref='answers')


"""
Links/notes
[1] SQLAlchemy multiple foreign keys in one mapped class to the same primary key
        https://stackoverflow.com/questions/22355890/sqlalchemy-multiple-foreign-keys-in-one-mapped-class-to-the-same-primary-key
    extra_SQLAlchemy Documentation-Basic Relationship Patterns-Many to many
        https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#many-to-many
    extra_SQLAlchemy - Multiple Foreign key pointing to same table same attribute
        https://stackoverflow.com/questions/44434410/sqlalchemy-multiple-foreign-key-pointing-to-same-table-same-attribute
    extra_SqlAlchemy Error on Creating multiple foreign key to one table
        https://stackoverflow.com/questions/53900595/sqlalchemy-error-on-creating-multiple-foreign-key-to-one-table
[2] https://youtu.be/HXV3zeQKqGY?t=15362
"""