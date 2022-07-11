# The Exam App!

#### Video Demo: https://youtu.be/BpNdRowgLF4

#### Description:

##### Introduction

​	This is a web app where students will give exams and teachers will check them and give marks accordingly. It has been designed and developed using Python and Flask for the backend and HTML, CSS(BootStrap) and JS for the frontend.

##### Motivation

​	The reason I chose this project idea is because, I saw a need for students to give online exams during the pandemic. In most schools of my country, regular exams were not being taken because of lack of an infrastructure through which a teacher could take exams of hundreds of students simultaneously, grade them, and return the graded papers (digital papers of course) back to the students. Normally, the teachers only give assignments to the students, which the students complete in a lackluster way. Furthermore, the students were copying from other classmates, there were no automatic deadline maintenance mechanism, no easy way to manage the assignments (the guardians would have to manually submit the assignments in person in the school campus etc. This app has been designed to tackle some of those issues.

##### Pages of the App

1. Register
2. Login
3. Dashboard (Teacher's)
4. Current Students (accessed by Teachers)
5. Your Questions (accessed by Teachers)
6. View all Submissions (accessed by Teachers)
7. Grading (accessed by Teachers)
8. Dashboard (Student's)
9. Give (Start) Exam (accessed by Students)

##### Structure of the App

​	In ***/the_exam_app*** directory, we have both the source code of the app and the database associated with it. In this directory, we have a file named **models.py**. This python file defines the structure of our database along with the relationship between the tables within it. Our database file is **dbx5.sqlite3** (forgive the file naming!).

​	In the ***/the_exam_app/routes*** directory, we have 3 python files,

- __ init__.py
- auth.py
- main.py

###### __ init__.py:

This python file initializes our whole app. This file also initializes the login manager and the database used in our app. We create a new database using the command line command **"flask create_tables"**, which is implemented using logic **app.cli.add_command(create_tables)** within this file.

###### auth.py:

This file does three things,

1. register a new user
2. login users
3. logout current user

###### main.py:

This file contains the main business logic of our app. It has the following logic blocks:

1. **teacher()** - It controls what features we have in the dashboard of a teacher. We add or remove subjects using this logic block.
2. **teacher_students()** - This block allows the teacher to add, remove and view students.
3. **teacher_questions()** - This block allows the teacher to add, remove and view questions.
4. **edit_question()** - This block allows the teacher to edit a question and set the exam start and end time.
5. **student()** - This block controls the structure of the student's dashboard. From this dashboard, the student can view his upcoming exams, as well as a list of all the subjects he is enrolled in.
6. **edit_answer()** - This block allows the student to edit and submit his answer to a particular question of a particular exam he is participating in.
7. **answers()** - This blocks displays all the answers of a particular question (of a particular exam), and grade those answers of each student.



​	In the ***the_exam_app/static*** directory, we have the CSS files that make our app look user-friendly. The JS codes required to control the timers of exam start and end times are written in JavaScript, but they are written within HTML files of the respective pages.

​	In the ***the_exam_app/templates*** directory, we have all the HTML files that structures our app, which we use to do Server-Side-Rendering. They are:

1. **register_way2.html**
2. **login.html**
3. **index_teacher.html**
4. **addorremove_students.html**
5. **addorremove_questions2.html**
6. **edit_question.html**
7. **index_student.html**
8. **edit_answer.html**
9. **answers.html**






