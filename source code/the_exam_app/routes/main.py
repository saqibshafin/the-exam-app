#from re import A
#from operator import xor
from flask import Blueprint, render_template, request, redirect, url_for
#from flask.helpers import url_for
#from flask_login.mixins import UserMixin
from flask_login import current_user, login_required
#from werkzeug.utils import redirect
#from sqlalchemy import tuple_
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, validators

from the_exam_app.extensions import db 
from ..models import User, Subject, Students_of_teacher, Question, Answer
# ".." goes up one level. "..."goes up two level. "..models" can also be written as
# app_name.models or, in this app, the_exam_app.models
#from __init__ import load_user

main = Blueprint('main', __name__)  # **OK**I dont understand how this line works.
# Check auth.py for the explanation.

"""@main.route("/", methods=["GET"])
def index():
    #return render_template('register.html')
    return ('<h1>hello<h1>')"""

"""@main.route('/', methods=['GET','POST'])
def index():  # index=home
    if request.method == 'POST':
        return render_template('index.html')
    else:
        return render_template('index.html')"""


@main.route('/teacher', methods=['GET','POST'])
@login_required
def teacher():  # index=home
    if request.method == 'POST':
        if request.form.get('add_or_delete') == "a":  # 'a' stands for add
            print("---------|-|-|-|-adding subject")
            name = request.form['new_subject']
            classs = request.form['classs']
            print("---------|-|-|-|", name, classs)
            # add new subject            
            subject_to_add = Subject(name=name, classs=classs, user_id=current_user.id)#load_user())#UserMixin.id)
            print("---------|-|-|-|",subject_to_add.id, subject_to_add.name, 
                subject_to_add.classs, subject_to_add.user_id)
            
            db.session.add(subject_to_add)
            db.session.commit()

        #elif request.form["add_subject"] is None:
        #http://127.0.0.1:5000/teacher&addsubject=phy
        elif request.form["add_or_delete"] == "d":  # 'd' stands for delete
            # delete a subject
            print("---------|-|-|-|-deleting subject")
            name = request.form['subject_to_delete']
            classs = request.form['classs_to_delete']
            print("---------|-|-|-|", name, classs)

            subject_to_delete = Subject.query.filter(Subject.name==name, 
                Subject.classs==classs, Subject.user_id==current_user.id).first()  # [1]
            print("---------|-|-|-|", subject_to_delete)
            print("---------|-|-|-|", subject_to_delete.id, subject_to_delete.name, 
                subject_to_delete.classs, subject_to_delete.user_id)

            db.session.delete(subject_to_delete)
            db.session.commit()

        """elif request.form["add_or_delete"] == "s":
            # return render_template('addorremove_students.html')
            return redirect(url_for('main.teacher_students'))"""
        
        return render_template('index_teacher.html')
    else:
        """a=User.query.all()
        print("-------------|-|-|-|",a)
        b=User.query.filter_by(name="1w").first()
        print("-------------|-|-|-|",b)
        c=b.name
        print("-------------|-|-|-|",c,b.subject, b.subject[1], b.subject[1].name)"""
        
        subjects = Subject.query.filter_by(user_id=current_user.id).all()
        #print("---------|-|-|-|",subject.id, subject.name, subject.classs, subject.user_id)
        subs_name = []
        subs_classs = []
        for subject in subjects:
            print("---------|-|-|-|",subject.id, subject.name, subject.classs, subject.user_id)
            subs_name.append(subject.name)
            subs_classs.append(subject.classs)
        print("---------|-|-|-|",subjects,subs_name,subs_classs)
        return render_template('index_teacher.html', subjects=subs_name, classes=subs_classs)


@main.route('/teacher/students', methods=['GET', 'POST'])
@login_required
def teacher_students():
    if request.method == 'POST':
        name = request.form['student']
        student = User.query.filter_by(name=name).first()  # multiple students might
            # have the same name. So add a "search by email" option        
        sub_name = request.form["subject_of_teacher"]
        sub_classs = request.form["classs_of_teacher"]
        selected_sub = Subject.query.filter_by(name=sub_name, classs=sub_classs).first()
        # **Why does filter_by work now for multiple filter parameters?
        print("-------------|-|-|-|",student.name, student.id, selected_sub.id, 
            selected_sub.name, selected_sub.classs, sub_name, sub_classs)

        if request.form["add_or_remove"] == "a":
            student_to_add = Students_of_teacher(teacher_id=current_user.id, student_id=student.id,
                subject_id=selected_sub.id)
            print("-------------|-|-|-|", student_to_add.teacher_id, student_to_add.student_id,
                student_to_add.subject_id)

            db.session.add(student_to_add)
            db.session.commit()

        elif request.form["add_or_remove"] == "r":
            student_to_remove = Students_of_teacher.query.filter_by(
                teacher_id=current_user.id, 
                student_id=student.id, 
                subject_id=selected_sub.id)\
                .first()
            #Students_of_teacher(teacher_id=current_user.id, student_id=student.id,
            #    subject_id=selected_sub.id)
            print("-------------|-|-|-|", student_to_remove.teacher_id, student_to_remove.student_id,
                student_to_remove.subject_id)

            db.session.delete(student_to_remove)
            db.session.commit()

        subjects = Subject.query.filter_by(user_id=current_user.id).all()        
        subs_name = []
        subs_classs = []
        for subject in subjects:
            #print("-------------|-|-|-|",subject.id, subject.name, subject.classs, subject.user_id)
            subs_name.append(subject.name)
            subs_classs.append(subject.classs)
        #print("-------------|-|-|-|",subjects,subs_name,subs_classs)

        #students_list = Students_of_teacher.query.filter_by(teacher_id=current_user.id).all()
        #for student in students_list:
        #    print("-------------|-|-|-|", student.teacher_id, student.student_id, 
        #        student.subject_id)
        sstudents_list = db.session.query(User, Students_of_teacher, Subject)\
            .filter(User.id == Students_of_teacher.student_id)\
            .filter(Subject.id == Students_of_teacher.subject_id)\
            .filter(Students_of_teacher.teacher_id == current_user.id)\
            .all()

        return render_template('addorremove_students.html', subjects=subs_name, classes=subs_classs,
            students_list=sstudents_list)
    else:
        subjects = Subject.query.filter_by(user_id=current_user.id).all()
        #print("---------|-|-|-|",subject.id, subject.name, subject.classs, subject.user_id)
        subs_name = []
        subs_classs = []
        for subject in subjects:
            print("-------------|-|-|-|",subject.id, subject.name, subject.classs, subject.user_id)
            subs_name.append(subject.name)
            subs_classs.append(subject.classs)
        print("-------------|-|-|-|",subjects,subs_name,subs_classs)

        #students_list = Students_of_teacher.query.filter_by(teacher_id=current_user.id).all()
        
        """
        # Ok, i didn't need the following snippet after all.
        # Ok, the previous line is wrong. It seems, the logic I
        # used matches with the following snippet.
        q = Session.query(
                User, Document, DocumentPermissions,
            ). filter(
                User.email == Document.author,
            ). filter(
                Document.name == DocumentPermissions.document,
            ). filter(
                User.email == 'someemail',
            ). all()"""
        
        sstudents_list = db.session.query(User, Students_of_teacher, Subject)\
            .filter(User.id == Students_of_teacher.student_id)\
            .filter(Subject.id == Students_of_teacher.subject_id)\
            .filter(Students_of_teacher.teacher_id == current_user.id)\
            .all()  # [2] [3]
                # 'sstudents_list' here is a list of 2 tuples.
        # https://docs.sqlalchemy.org/en/14/orm/tutorial.html#querying-with-joins 
            # The actual SQL JOIN syntax, on the other hand, is most easily achieved
            # using the Query.join() method:

            #    SQL>>> session.query(User).join(Address).\
            #    ...         filter(Address.email_address=='jack@google.com').\
            #    ...         all()
            #    [<User(name='jack', fullname='Jack Bean', nickname='gjffdd')>]
            # https://docs.sqlalchemy.org/en/14/orm/tutorial.html#querying-with-joins           
        #for a,b in sstudents_list:
        #    print(a)
        #    print(b)
        for student in sstudents_list:  # "student" is atuple, and "sstudents_list"
        # is a list of multiple(in this case, 3) tuples.
            #print("-------------|-|-|-|", student)
            #print("-------------|-|-|-|", student[0], student[1])
            print("-------------|-|-|-|", 
                student[0].id, student[0].name, student[0].email,
                student[1].subject_id,
                student[2].name
            )

        # [4] Using Joins
        """sstudents_list = db.session.query(User, Students_of_teacher)\
            .join(Students_of_teacher.students_of_teacher)\
            .filter(User.id == Students_of_teacher.student_id)\
            .filter(Students_of_teacher.teacher_id == current_user.id)\
            .all()  # This works too. Then, what is the difference between this and
            # the previous "sstudents_list"? Also, 'sstudents_list' here 
            # is a list of 2 tuples.
        # https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.join
        #for a,b in sstudents_list:
        #    print("-------------|-|-|-|", a)
        #    print("-------------|-|-|-|", b)
        for student in sstudents_list:
            #print("-------------|-|-|-|", student.teacher_id, student.name, student.id,
            #    student.student_id, student.subject_id)
            #print("-------------|-|-|-|", student)  # same as saying print(a) and print(b)
            print("-------------|-|-|-|", student[0], student[1])
            print("-------------|-|-|-|", student[0].id, student[0].name,
                student[0].email,
                student[1].subject_id)"""

        return render_template('addorremove_students.html', subjects=subs_name, classes=subs_classs,
            students_list=sstudents_list)


@main.route('/teacher/questions', methods=['GET','POST'])
@login_required
def teacher_questions():
    if request.method == 'POST':
        name = request.form['exam_type']       
        sub_name = request.form["subject_of_teacher"]
        sub_classs = request.form["classs_of_teacher"]
        selected_sub = Subject.query.filter_by(name=sub_name, classs=sub_classs).first()
        #question_to_add0 = Question(name=name, subject_id=selected_sub.id)
        #print("-------------|-|-|-|",question_to_add0.name, question_to_add0.id, selected_sub.id, 
        #    selected_sub.name, selected_sub.classs, sub_name, sub_classs)

        if request.form["add_or_remove"] == "a":
            question_to_add = Question(name=name, subject_id=selected_sub.id)

            db.session.add(question_to_add)
            added_question = Question.query\
                .filter_by(name=name, subject_id=selected_sub.id)\
                .first()
            # 'added_question' makes sure we select the first subject that matches
            # our search criteria. Also, using this value, we can monitor if 
            # same questions are being created again or not{not implemented yet},
            # by using ".all()"
            print("-------------|-|-|-|",added_question)

            """people_who_have_access = db.session.query(Students_of_teacher)\
                .filter(Students_of_teacher.subject_id == selected_sub.id)\
                .filter(Students_of_teacher.teacher_id == current_user.id)\
                .all()"""
                # The above 'people_who_have_access' is same as the 
                # query below.
            people_who_have_access = Students_of_teacher.query\
                .filter_by(subject_id = selected_sub.id)\
                .filter_by(teacher_id = current_user.id)\
                .all()
            # These following queries didn't work as expected.
            """x = db.session.update(Students_of_teacher)\
                .where(Students_of_teacher.subject_id == selected_sub.id)\
                .where(Students_of_teacher.teacher_id == current_user.id)\
                .values(question_access_id = question_to_add.id) """
            """x = Students_of_teacher.query\
                .filter_by(subject_id = selected_sub.id)\
                .filter_by(teacher_id = current_user.id)\
                .update(dict(question_access_id = question_to_add.id))"""
            """x = db.session.query(Students_of_teacher)\
                .filter_by(subject_id = selected_sub.id)\
                .filter_by(teacher_id = current_user.id)\
                .update(dict(question_access_id = question_to_add.id))"""

            # Trying raw SQL within Flask-SQLAlchemy
            # x = db.session.execute('SELECT * FROM Students_of_teacher WHERE teacher_id = :val', {'val': 6})
            print("-------------|-|-|-|", people_who_have_access)
            for row in people_who_have_access:
                #row.question_access_id = question_to_add.id  # this line is
                    # different from the next line in the sense that this line
                    # assigns the latest question (that has been inserted just
                    # now in the question table) to the "row.question_access_id"
                row.question_access_id = added_question.id
                print("-------------|-|-|-|", row, question_to_add, question_to_add.id,
                    added_question, added_question.id)
            print("-------------|-|-|-|", people_who_have_access)

            db.session.commit()  # Note that, we didn't need to do a
            # separate db.session.add(added_question). I don't know why.

        elif request.form["add_or_remove"] == "r":
            name = request.form['exam_type']       
            sub_name = request.form["subject_of_teacher"]
            sub_classs = request.form["classs_of_teacher"]
            selected_sub = Subject.query.filter_by(name=sub_name, classs=sub_classs).first()
            question_to_remove = Question.query.filter_by(name=name, 
                subject_id=selected_sub.id).first()
                # or .all()
            print("-------------|-|-|-|",question_to_remove, selected_sub)
            people_who_donthave_access = Students_of_teacher.query\
                .filter_by(subject_id = selected_sub.id)\
                .filter_by(teacher_id = current_user.id)\
                .all()
                # or, filter_by(question_access_id = question_to_remove.id) in place of
                # filter_by(subject_id = selected_sub.id
            for row in people_who_donthave_access:
                #row.question_access_id = question_to_add.id
                row.question_access_id = None
                print("-------------|-|-|-|", row, row.question_access_id)

            db.session.delete(question_to_remove)
            db.session.commit()

        subjects = Subject.query.filter_by(user_id=current_user.id).all()        
        subs_name = []
        subs_classs = []
        for subject in subjects:
            #print("-------------|-|-|-|",subject.id, subject.name, subject.classs, subject.user_id)
            subs_name.append(subject.name)
            subs_classs.append(subject.classs)
        #print("-------------|-|-|-|",subjects,subs_name,subs_classs)

        questions_list = db.session.query(Question, Subject)\
            .filter(Subject.user_id == current_user.id)\
            .filter(Question.subject_id == Subject.id)\
            .all()
        for question in questions_list:
            print("-------------|-|-|-|", question)

        return render_template('addorremove_questions2.html', subjects=subs_name, classes=subs_classs,
            questions_list=questions_list)
    else:
        subjects = Subject.query.filter_by(user_id=current_user.id).all()
        #print("---------|-|-|-|",subject.id, subject.name, subject.classs, subject.user_id)
        subs_name = []
        subs_classs = []
        for subject in subjects:
            print("-------------|-|-|-|",subject.id, subject.name, subject.classs, subject.user_id)
            subs_name.append(subject.name)
            subs_classs.append(subject.classs)
        print("-------------|-|-|-|",subjects,subs_name,subs_classs)

        questions_list = db.session.query(Question, Subject)\
            .filter(Subject.user_id == current_user.id)\
            .filter(Question.subject_id == Subject.id)\
            .all()
        for question in questions_list:
            print("-------------|-|-|-|", question)

        return render_template('addorremove_questions2.html', subjects=subs_name, classes=subs_classs,
            questions_list=questions_list)


# Question Form Class  # [6] WTForms youtube+github
class QuestionForm(FlaskForm):
    #title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])


# edit_question, way 1
"""@main.route('/edit_question', methods=['GET','POST'])
@login_required
def edit_question():
    if request.method == 'POST':
        if request.form["add_or_remove"] == "ei":  # e = question edit_initialised
            question_id = request.form["question_id"]
            question = Question.query.filter_by(id=question_id).first()
            
            form = QuestionForm(request.form)
            form.body.data = question.question

            print("-------------|-|-|-|", form, form.body, form.body.data,
                question, question.question)
            return render_template('edit_question.html', form=form, question_id=question_id)

        elif request.form["add_or_remove"] == "ed":  # e = question edit_done
            question_id = request.form["question_id"]
            question = Question.query.filter_by(id=question_id).first()
            print("-------------|-|-|-|", question, question.question, question_id)
            question.question = request.form["body"]
            print("-------------|-|-|-|", question, question.question, question_id)

            db.session.commit()
            
            return redirect(url_for('main.teacher_questions'))

        elif request.form["add_or_remove"] == "r":
            question_id = request.form["question_id"]
            question_to_remove = Question.query.filter_by(id=question_id).first()
            print("-------------|-|-|-|",question_to_remove, question_to_remove.id, 
                question_to_remove.question)
            
            db.session.delete(question_to_remove)
            db.session.commit()

            return redirect(url_for('main.teacher_questions'))

    else:
        #question_id = request.form["question_id"]
        #question = Question.query.filter_by(id=question_id).first()
        
        #form = QuestionForm(request.form)
        #form.body.data = question.question

        #print("-------------|-|-|-|", form.body, question, question.question )
        #if QuestionForm(request.form) is None:
        #    form = None
        #return render_template('edit_question.html')#, form=form)
        
        #!!the Get request should not work in edit_questions, for now."""


# edit_question, way 2.
#@main.route('/edit_question', methods=['GET','POST'])
@main.route('/edit_question/<string:id>', methods=['GET','POST'])  #**I declared "id" type 
    #as string, even though it is an int in the database...
@login_required
def edit_question(id):
    if request.method == 'POST':
        # Needed the first "if" when I used addorremove_questions.html
        
        """if request.form["add_or_remove"] == "ei":  # e = question edit_initialised
            question_id = request.form["question_id"]
            question = Question.query.filter_by(id=question_id).first()
            
            form = QuestionForm(request.form)
            form.body.data = question.question

            print("-------------|-|-|-|", form, form.body, form.body.data,
                question, question.question)
            return render_template('edit_question.html', form=form, question_id=question_id)"""

        # Edit a question
        if request.form["add_or_remove"] == "ed":  # ed = question edit_done
            # edit_question.html triggers this "if" statement
            
            question_id = request.form["question_id"]
            # question_id = id  # This also works, see the html file.
            date = request.form["examstart_date"]  # [5]
            time = request.form["examstart_time"]  # [5]
            examstart_datetime = date + ' ' + time
            print("-------------|-|-|",date,time, type(date), type(time), 
                examstart_datetime, type(examstart_datetime))

            date = request.form["examend_date"]  # [5]
            time = request.form["examend_time"]  # [5]
            examend_datetime = date + ' ' + time
            print("-------------|-|-|",date,time, type(date), type(time), 
                examend_datetime, type(examend_datetime))

            question = Question.query.filter_by(id=question_id).first()
            print("-------------|-|-|-|", question, question.question, question_id)
            question.question = request.form["body"]
            question.examstart_datetime = examstart_datetime
            question.examend_datetime = examend_datetime
            print("-------------|-|-|-|", question, question.question, question_id)

            db.session.commit()
            
            return redirect(url_for('main.teacher_questions'))

        # Removing questions will only be done from "main.teacher_question"
        """elif request.form["add_or_remove"] == "r":
            # "Delete" button in the questions table of addorremove_questions1.html 
            # triggers this "if" statement
            
            question_id = id
            question_to_remove = Question.query.filter_by(id=question_id).first()
            print("-------------|-|-|-|",question_to_remove, question_to_remove.id, 
                question_to_remove.question)
            
            db.session.delete(question_to_remove)
            db.session.commit()

            return redirect(url_for('main.teacher_questions'))"""

    # View a question
    else:
        # The "Edit" button in the questions table of addorremove_questions1.html
        # triggers this "else" statement
        
        question_id = id
        question = Question.query.filter_by(id=question_id).first()
        
        form = QuestionForm(request.form)
        form.body.data = question.question

        print("-------------|-|-|-|", form, form.body, form.body.data,
            question, question.id, question.question)
        """if QuestionForm(request.form) is None:
            form = None"""
        return render_template('edit_question.html', id=id, 
                form=form, question_id=question_id)
            # Not using the "question_id=question_id" variable.


@main.route('/student', methods=['GET','POST'])
@login_required
def student():  # index=home
    if request.method == 'POST':
        # if request.form["add_or_remove"] == "ed":  # ed = question edit_done
        #     # edit_question.html triggers this "if" statement
            
        #     question_id = request.form["question_id"]
        #     # question_id = id  # This also works, see the html file.
        #     date = request.form["exam_date"]  # [5]
        #     time = request.form["exam_time"]  # [5]
        #     exam_datetime = date + ' ' + time
        #     print("-------------|-|-|",date,time, type(date), type(time), 
        #         exam_datetime, type(exam_datetime))

        #     question = Question.query.filter_by(id=question_id).first()
        #     print("-------------|-|-|-|", question, question.question, question_id)
        #     question.question = request.form["body"]
        #     question.exam_datetime = exam_datetime
        #     print("-------------|-|-|-|", question, question.question, question_id)

        #     db.session.commit()
            
        #     return redirect(url_for('main.edit_answer'))
        return render_template('index_student.html')
    else:
        """subjects_list = db.session.query(User, Students_of_teacher, Subject)\
            .filter(Students_of_teacher.student_id == current_user.id)\
            .filter(User.id == Students_of_teacher.teacher_id)\
            .filter(Subject.id == Students_of_teacher.subject_id)\
            .all()
        exams_list = db.session.query(
            User, Students_of_teacher, Subject, Question)\
            .filter(Students_of_teacher.student_id == current_user.id)\
            .filter(User.id == Students_of_teacher.teacher_id)\
            .filter(Subject.id == Students_of_teacher.subject_id)\
            .filter(Question.subject_id == Students_of_teacher.subject_id)\
            .all()"""
        # Using subjectplusexam_list instead of subjects_list and exams_list
        # subjectPlusExam_list = db.session.query(
        #     User, Students_of_teacher, Subject, Question, Answer)\
        #     .filter(Students_of_teacher.student_id == current_user.id)\
        #     .filter(User.id == Students_of_teacher.teacher_id)\
        #     .filter(Subject.id == Students_of_teacher.subject_id)\
        #     .filter(Question.id == Students_of_teacher.question_access_id)\
        #     .filter(Answer.question_id == Question.id)\
        #     .filter(Answer.user_id == current_user.id)\
        #     .order_by(Question.examstart_datetime.asc())\
        #     .all()#.filter(Question.subject_id == Students_of_teacher.subject_id)\
        subjectPlusExam_list = db.session.query(
            User, Students_of_teacher, Subject, Question)\
            .filter(Students_of_teacher.student_id == current_user.id)\
            .filter(User.id == Students_of_teacher.teacher_id)\
            .filter(Subject.id == Students_of_teacher.subject_id)\
            .filter(Question.id == Students_of_teacher.question_access_id)\
            .order_by(Question.examstart_datetime.asc())\
            .all()#.filter(Question.subject_id == Students_of_teacher.subject_id)\
        #return render_template('index_student.html', subjects_list=subjects_list,
        #    exams_list=exams_list)

        # print("-------------|-|-|-|", subjectPlusExam_list[0], len(subjectPlusExam_list))
        print("-------------|-|-|-|", len(subjectPlusExam_list))

        return render_template('index_student.html', subjectPlusExam_list=subjectPlusExam_list)


# @main.route('/questions')  # This page will display the questions written by a
# teacher(viewed either by the teacher(user) or the students(user))
@login_required
def questions():
    return render_template('questions.html')


# Question Form Class
class AnswerForm(FlaskForm):
    #title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])


@main.route('/edit_answer/<string:id>', methods = ['GET', 'POST'])
@login_required
def edit_answer(id):
    if request.method == 'POST':
        if request.form['add_or_remove'] == "view":  # View question & empty answer_form
            answer = Answer.query\
                .filter_by(question_id=id)\
                .filter_by(user_id=current_user.id)\
                .first()
            print("-------------|-|-|-|", answer)#, answer.id)

            if answer is None:
                empty_answer = Answer(question_id=id, user_id=current_user.id)

                db.session.add(empty_answer)
                
                answer = Answer.query\
                    .filter_by(question_id=id)\
                    .filter_by(user_id=current_user.id)\
                    .first()
                print("-------------__/\__/\__", answer, answer.id)

            # answer = Answer.query.filter_by(id=answer_id).first()
            
            form = AnswerForm(request.form)
            form.body.data = answer.answer

            # print("-------------|-|-|-|", form, form.body, form.body.data,
            #     answer, answer.id, answer.answer)
            # """if QuestionForm(request.form) is None:
            #     form = None"""

            db.session.commit()

            question = Question.query.filter_by(id=id).first()
            return render_template('edit_answer.html', question=question, id=id, 
                    form=form, answer_id=answer.id)
            # [7] <p>{{ question | safe }}</p>

        if request.form["add_or_remove"] == "ed":  # ed = answer edit_done
            # edit_answer.html triggers this "if" statement            
            
            answer_id = id

            answer = Answer.query.filter_by(id=answer_id).first()
            print("-------------|-|-|-|", answer, answer.answer, answer.id)
            answer.answer = request.form["body"]
            print("-------------|-|-|-|", answer, answer.answer, answer.id)

            db.session.commit()
            
            return redirect(url_for('main.student'))
    else:
        
        return render_template('edit_answer.html')


@main.route('/answers/<string:id>', methods = ['GET', 'POST'])  # the answers page(of a 
# particular question) could be seen by the teachers or seen by the students which they 
# had answered(of a particular question)
# @main.route('/answers/question/<string:id>', methods = ['GET', 'POST'])
# @main.route('/answers/answer/<string:id>', methods = ['GET', 'POST'])
@login_required
def answers(id):
    if request.method == "POST":
        if request.form["add_or_remove"] == "check":
            answer = Answer.query.filter_by(id=id).first()
            question = Question.query.filter_by(id=answer.question_id).first()
            print("-------------|-|-|-|", answer.id, question.id, question.total_marks)
            return render_template('answer_ofthe_student.html', answer=answer, question=question)
        elif request.form["add_or_remove"] == "checked":
            marksAttained = request.form["marksAttained"]
            print("-------------|-|-|-|", marksAttained)

            answer = Answer.query.filter_by(id=id).first()
            answer.marks_attained = marksAttained
            print("-------------|-|-|-|", answer.marks_attained)
            db.session.add(answer)
            db.session.commit()
            
            question = Question.query.filter_by(id=answer.question_id).first()
            return redirect(url_for("main.answers", id = question.id))
        else:
            return None  # note the return value
    else:
        question = Question.query.filter_by(id=id).first()
        # students_list = db.session.query(User, Students_of_teacher, Question, Answer)\
        students_list = db.session.query(User, Answer)\
            .filter(Answer.question_id == question.id)\
            .filter(User.id == Answer.user_id)\
            .all()  # question.id is same as "id", it should be obvious
            # .filter(Students_of_teacher.id == question.id)\
            # .filter(Students_of_teacher.teacher_id == current_user.id)\
            # .filter(Subject.id == Students_of_teacher.subject_id)\
        return render_template('answers.html', question=question, students_list=students_list)



"""
Links/notes
[1] https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.filter
[2] Querying with Joins
        https://docs.sqlalchemy.org/en/14/orm/tutorial.html#querying-with-joins
    sqlalchemy: how to join several tables by one query?
        https://stackoverflow.com/questions/6044309/sqlalchemy-how-to-join-several-tables-by-one-query
    Flask SQL Alchemy Query Join Multiple Tables
        https://www.onooks.com/flask-sqlalchemy-creating-query-to-join-multiple-tables/
[3] 7. Query properties:
      Certain web frameworks (I'm looking at you, Flask-SQLAlchemy!) promote the use of query properties
    that supposedly make querying easier. Trouble is, it is apparently not obvious from the example code 
    how one would query for specific columns, aggregates or other expressions using said query property.
      The solution is to use the session directly:
        db.session.query(Company.address)
        https://alextechrants.blogspot.com/2013/11/10-common-stumbling-blocks-for.html
[4] 8. Attempting to access related classes through relationships in queries:
      
      Someone asks something like this every week on #sqlalchemy:
        <anon> anyone see anything wrong with this query: 
        c = Category.query.join(Category.parent)\
            .filter(Category.name=='Social Issues', Category.parent.name=='Teens')\
            .first()
      
      What is wrong with this query is of course that Category.parent is a relationship and thus it 
    doesn't have a "name" attribute. I don't blame anyone who falls for this though. It would make
    sense, from the syntactic perspective, for this to work. It might automatically add a join to 
    Category.parent in the query. The reason why this can't be done is beyond my knowledge of 
    SQLAlchemy. Anyway, to fix the query, you add an alias and join that:

    parent = aliased(Category)
        c = Category.query.join(parent, Category.parent)\
            .filter(Category.name=='Social Issues', parent.name=='Teens')\
            .first()
        https://alextechrants.blogspot.com/2013/11/10-common-stumbling-blocks-for.html
[5] Datatypes In SQLite Version 3
        https://www.sqlite.org/datatype3.html
    Date And Time Functions
        https://www.sqlite.org/lang_datefunc.html

        https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/date
        https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/time
[6] WTForms
[7] I think you are trying to render the body as html not as text. jinja autoescapes the text , you can 
        stop autoescaping, For that you can use the safe filter of jinja.
            <p>{{ question | safe }}</p>
        https://stackoverflow.com/questions/68356141/python-flask-blog-message-without-format
    Controlling Autoescaping - PalletsProjects
        https://flask.palletsprojects.com/en/2.0.x/templating/#controlling-autoescaping
[8] 
"""