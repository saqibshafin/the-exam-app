from flask import Blueprint, render_template, redirect, request, url_for, session, json
from flask_login import login_user, logout_user, current_user
# from sqlalchemy.sql.elements import Null
from werkzeug.security import check_password_hash

from the_exam_app.extensions import db 
from ..models import User

auth=Blueprint('auth',__name__)  # why this line?
# [3] 'auth' is a Blueprint object.


# Register, way 1
"""@auth.route('/register_type', methods=['GET', 'POST'])
def register_type():
    if request.method == 'POST':
        register_type = request.form['selected_register_type']
        print(register_type)

        #register_type = json.dumps({"main":"Condition failed on page baz"})
        session['register_type'] = register_type    # [1]

        return redirect(url_for("auth.register", register_type=register_type))    # [1]
        #return redirect(url_for("auth.register"))
    else:
        register_types = ["Admin", "Teacher", "Student"]
        return render_template("register_chooseaccounttype.html", register_types=register_types)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':         
        name = request.form['name']
        unhashed_password = request.form['password']
        # the reason we used request.form[] instead of request.form.get(), is 
    # because we want it to fail if the form is empty.

        register_type = request.form['register_type']  # [2] <input type="hidden" id="register" name="register_type" value="{{ register_type}}">
        print("apes",register_type)
        if register_type=='Admin':
            adm = True
            tea = False
            stud = False
        elif register_type=='Teacher':
            adm = False
            tea = True
            stud = False
        elif register_type=='Student':
            adm = False
            tea = False
            stud = True

        user = User(name=name, unhashed_password=unhashed_password, admin=adm, teacher=tea)
        # What we are doing is, we are not directly passing the original password
    # to the db, we are instead passing in 'unhashed_password', which automatically
    # gets converted to a hashed password, due to the 'unhashed_password.setter' 
    # in 'models.py' 

        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login"))
        #return redirect("/")
    else:
        #print(request.form['register_type'])

        register_type = request.args['register_type']  # counterpart for url_for()    # [1]
        #register_type = session['register_type']       # counterpart for session    # [1]
        print('monky',register_type)

        if register_type=='Admin':
            return render_template('register.html', x='an', register_type=register_type)
        elif register_type=='Teacher':
            return render_template('register.html', x='a', register_type=register_type)
        elif register_type=='Student':
            return render_template('register.html', x='a', register_type=register_type)
"""

# Register, way 2
@auth.route('/register', methods=['GET', 'POST'])  #**Beware, I didn't implement the password comparison...
def register():
    if request.method == 'POST':         
        name = request.form['name']
        email = request.form['email']
        unhashed_password = request.form['password']
        # the reason we used request.form[] instead of request.form.get(), is 
    # because we want it to fail if the form is empty.

        register_type = request.form['selected_register_type']
        print("---------|-|-|-|apes",register_type)
        if register_type=='Admin':
            adm = True
            tea = False
            stud = False
        elif register_type=='Teacher':
            adm = False
            tea = True
            stud = False
        elif register_type=='Student':
            adm = False
            tea = False
            stud = True

        #user = User(name=name, unhashed_password=unhashed_password, teacher=tea, student=stud)  # admin=adm
        user = User(name=name, email=email,unhashed_password=unhashed_password, teacher=tea, student=stud)
        # What we are doing is, we are not directly passing the original password
    # to the db, we are instead passing in 'unhashed_password', which automatically
    # gets converted to a hashed password, due to the 'unhashed_password.setter' 
    # in 'models.py' 

        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login"))
        #return redirect("/")
    else:
        current_user.id = False    
        print("-------------__/\__/\__",current_user , current_user.id, )

        register_types = ["Admin", "Teacher", "Student"]
        return render_template("register_way2.html", register_types=register_types)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        #name = request.form['name']
        email = request.form["email"]
        password = request.form['password']
        print("---------|-|-|-|apes",email,password)

        #user = User.query.filter_by(name=name).first()
        user = User.query.filter_by(email=email).first()
        print("---------|-|-|-|apes",user)
        #print("|-|-|-|apes",user.id,user.name,user.password,user.admin,user.teacher)

        error_message = ''  # it is kept empty.

        if not user or not check_password_hash(user.password, password):
            error_message = 'Could not login. Please check your Username and Password.'
            # in the last line, we assign a value to the variable 'error_message'.
            print("---------|-|-|-|apes",error_message)
            return render_template('login.html')

        if not error_message:  # means, if the error_message is not empty, execute this
        # if block.
            login_user(user)

            if user.teacher == True:
                return redirect(url_for('main.teacher'))
            elif user.student == True:
                return redirect(url_for('main.student'))
            else:
                return redirect(url_for('main.admin'))

            #return render_template('login.html')
            #return redirect("/")            
            #return redirect(url_for('main.index'))

    else:
        current_user.id = False    
        print("-------------__/\__/\__",current_user , current_user.id, )

        return render_template('login.html')

@auth.route('/logout')
def logout():
    # implement TODO: add the logout feature that will make current_user.teacher 
    #and current_user.student both null.

    # return redirect(url_for("auth.login"))

    # current_user = None
    # current_user.id = None    
    current_user.id = False   

    # logout_user

    print("-------------__/\__/\__",current_user , current_user.id, )
    #     current_user.teacher, current_user.student)
    return redirect("/login")


"""
Links/notes
[1] https://stackoverflow.com/questions/17057191/redirect-while-passing-arguments
[2] https://www.w3schools.com/tags/att_input_type_hidden.asp
    The <input type="hidden"> defines a hidden input field.
    A hidden field let web developers include data that cannot be seen or modified by users when a form is submitted.
    A hidden field often stores what database record that needs to be updated when the form is submitted.
    Note: While the value is not displayed to the user in the page's content, it is visible (and can be edited) using 
    any browser's developer tools or "View Source" functionality. Do not use hidden inputs as a form of security!
[3] Intro to Flask Blueprints - PrettyPrinted
    https://youtu.be/pjVhrIJFUEs
[4] 
"""