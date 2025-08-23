# application.py
#
# Name: Sliem el Ela
# Student number: 11248203
# Course: Web App Studio (Lente)

import hashlib
import os
import re
import numpy as np

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import *
from datetime import date, datetime

# Configure Flask app
app = Flask(__name__)

# Configure database
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Configure session, use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure migrations
Migrate(app, db)

# Secret key
app.secret_key = os.environ['SECRET_KEY']

# Configure admin interface
admin = Admin(app, name='IBOS', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(School, db.session))
admin.add_view(ModelView(SchoolLevel, db.session))
admin.add_view(ModelView(GroupTime, db.session))
admin.add_view(ModelView(TestType, db.session))

# Configuring flask Login
login_manager = LoginManager()
login_manager.init_app(app)

# Method for loading user
@login_manager.user_loader
def load_user(userID):
    return User.query.get(int(userID))

# Password validation for signing up.
def pass_validation(password):
    if len(password) < 8:
        return [False, "Make sure your password has at least 8 characters."]
    elif re.search("[0-9]", password) is None:
        return [False, "Make sure your password has number in it."]
    elif re.search("[A-Z]", password) is None:
        return [False, "Make sure your password has a capital letter in it."]
    elif re.search("[a-z]", password) is None:
        return [False, "Make sure your password has a lowercase letter in it."]
    elif re.search(r"\W", password) is None:
        return [False, "Make sure your password has a special character in it."]
    else:
        return [True, "No Error"]

# Home page
@app.route("/")
def index():
    """ Landing Page """
    return render_template("index.html")

# User registration
@app.route("/signup", methods=["GET", "POST"])
def signup():
    """ Signing up users """

    # Retrieving list of schools, levels and years
    schools = School.query.all()
    schoolLevels = SchoolLevel.query.all()
    schoolYears = SchoolYear.query.all()

    if request.method == "POST":

        # Retrieving user input
        username = request.form.get("username")
        password = request.form.get("password")
        firstName = request.form.get("first_name")
        lastName = request.form.get("last_name")
        email = request.form.get("email")
        role = request.form.get("role")
        school = request.form.get("school")
        schoolLevel = request.form.get("schoolLevel")
        schoolYear = request.form.get("schoolYear")

        # Booleans for role of user
        student = parent = False
        if role == "student":
            student = True
        elif role == "parent":
            parent = True 
            school = schoolLevel = schoolYear = None

        # Hashing password
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode("utf-8"), salt, 100000)

        # Inserting information into database
        user = User(username = username, firstName = firstName, lastName = lastName, email = email, key = key, salt = salt, \
            student = student, parent = parent, tutor = False, admin = False, schoolID = school, levelID = schoolLevel, yearID = schoolYear)
        db.session.add(user)
        db.session.commit()

        # Logging in user
        login_user(user)
        if user.admin:
            return redirect(url_for("portal"))
        elif user.tutor:
            return redirect(url_for("tutor"))
        elif user.parent:
            return redirect(url_for("parent", userID=current_user.id))
        else:
            return redirect(url_for("student", userID=current_user.id))

    return render_template("signup.html", schools = schools, schoolLevels = schoolLevels, schoolYears = schoolYears)

# Routes that are used for signup validation
@app.route("/usernamecheck", methods=["POST"])
def usernamecheck():
    """ Checking if username is already taken or has more then three characters """

    # Retrieving username
    username = request.form.get("username")

    # Checking if username is aready taken
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return jsonify({"username_success": False, "message": "That username is already taken."})

    # Checking if username has more than 3 characters
    elif len(username) < 4:
        return jsonify({"username_success": False, "message": "A username has to have more than three characters."})

    return jsonify({"username_sucess": True})

@app.route("/passwordcheck", methods=["POST"])
def passwordcheck():
    """ Checking if password satisfies requirements """

    # Retrieving password
    password = request.form.get("password")

    # Checking if password satisfies the requirements
    if pass_validation(password)[0] == False:
        return jsonify({"password_success": False, "message": pass_validation(password)[1]})
    else:
        return jsonify({"password_success": True, "message": pass_validation(password)[1]})

@app.route("/passwordcrossvalidation", methods=["POST"])
def passwordcrossvalidation():
    """ Checking if password and repeated password are the same """

    # Retrieving password information
    password = request.form.get("password")
    password_repeat = request.form.get("password_repeat")

    if password != password_repeat:
        return jsonify({"password_success": False, "message": "The passwords do not match!"})
    else:
        return jsonify({"password_success": True, "message": "Looks good!"})

@app.route("/emailcheck", methods=["POST"])
def emailcheck():
    """ Checking if email is unique """

    # Retrieving email information 
    email = request.form.get("email")
    user = User.query.filter_by(email=email).first()

    if user is not None:
        email_available = False
        return jsonify({"email_available": False, "message": "This e-mail is already in use."})
    else:
        return jsonify({"email_available": True})

@app.route("/login", methods=["GET", "POST"])
def login():
    """ Page for logging in a user """

    if request.method == "POST":

        # Retrieving user input
        username = request.form.get("username")
        password = request.form.get("password")

        # Retrieving user information
        user = User.query.filter_by(username=username).first()

        # Checking if user input is valid
        if user is None:
            flash("Username or password is incorrect!", "warning")
            return redirect(url_for("login"))

        # Retrieving salt and generating corresponding key
        salt = user.salt
        key = hashlib.pbkdf2_hmac('sha256', password.encode("utf-8"), salt, 100000)
        if user.key != key:
            flash("Username or password is incorrect!", "warning")

        # Logging in user
        else:
            login_user(user)
            if user.admin:
                return redirect(url_for("portal"))
            elif user.tutor:
                return redirect(url_for("tutor"))
            elif user.parent:
                return redirect(url_for("parent", userID=current_user.id))
            else:
                return redirect(url_for("student", userID=current_user.id))

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    """ Logging out the user """

    logout_user()
    return redirect(url_for("index"))

# Admin portal routes
@app.route("/portal")
@login_required
def portal():
    """ 
    Portal for admin users. 
    This route gives an overview of all accounts on which you can also change properties/permissions of certain users.
    """

    # Checking if current user is permitted to visit page
    if current_user.admin == False:
        return render_template("404.html")

    # Retrieve all users
    users = User.query.all()

    # Retrieving list of schools, levels and years
    schools = School.query.all()
    schoolLevels = SchoolLevel.query.all()
    schoolYears = SchoolYear.query.all()

    return render_template("portal.html", users=users, schools=schools, schoolLevels=schoolLevels, schoolYears=schoolYears)

@app.route("/portal/update", methods=["POST"])
@login_required
def update():
    """ Update user information """

    # Retrieve user information
    userID = request.form.get("userID")
    user = User.query.get(userID)

    # Retrieve new input by admin
    username = request.form.get("username")
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    schoolID = request.form.get("school")
    levelID = request.form.get("schoolLevel")
    yearID = request.form.get("schoolYear")
    roles = request.form.getlist("role")

    # Check the roles of user
    admin = tutor = parent = student = False 
    if "admin" in roles:
        admin = True
    if "tutor" in roles:
        tutor = True
    if "parent" in roles:
        parent = True
    if "student" in roles:
        student = True

    # Update userinformation
    user.username = username
    user.firstName = firstName
    user.lastName = lastName
    user.schoolID = schoolID
    user.levelID = levelID
    user.yearID = yearID
    user.student = student
    user.parent = parent
    user.tutor = tutor
    user.admin = admin 

    # Commit the changes
    db.session.commit()

    return redirect(url_for("portal"))

# Tutor routes
@app.route("/portal/tutor")
@login_required
def tutor():
    """ 
    Portal for tutor users. 
    This route gives an overview of all students on which you can also change certain properties of the student accounts.
    """
    
    # Checking is current user is permitted to visit page
    if current_user.admin == False and current_user.tutor == False:
        return render_template("404.html")

    # Retrieving list of schools, levels and years
    schools = School.query.all()
    schoolLevels = SchoolLevel.query.all()
    schoolYears = SchoolYear.query.all()

    # Retrieve info about all students
    students = User.query.filter_by(student=True).all()
    groups = GroupTime.query.all()

    return render_template("portal-tutor.html", students=students, groups=groups, schools=schools,\
        schoolLevels=schoolLevels, schoolYears=schoolYears)

@app.route("/portal/tutor/update", methods=["POST"])
def tutorUpdate():
    """ Updating the information of a student """

    # Retrieving user input
    studentID = request.form.get("student")
    groupID = request.form.get("group")
    schoolID = request.form.get("school")
    levelID = request.form.get("schoolLevel")
    yearID = request.form.get("schoolYear")

    # Changing user information
    student = User.query.get(studentID)
    student.schoolID = schoolID
    student.levelID = levelID
    student.yearID = yearID

    # Adding student to a group if student was groupless
    studentGroup = StudentGroup.query.filter_by(studentID=studentID).first()
    if studentGroup is None:
        studentGroup = StudentGroup(groupID=groupID, studentID=studentID)
        db.session.add(studentGroup)
    else:
        studentGroup.groupID = groupID
    
    db.session.commit()

    return redirect(url_for('tutor'))
    
# Parent and student routes
@app.route("/portal/parent/<int:userID>")
def parent(userID):
    """ 
    Portal for parent users. 
    This route gives an overview of all accounts that are children of the parent.
    You can also add new accounts via a relationship request.
    """

    # Retrieve information about parent
    parent = User.query.get(userID)

    # Check if the user is actually a parent 
    if parent is None or parent.parent == False:
        return render_template("404.html")

    # Checking is current user is permitted to visit page
    if current_user.admin == False and current_user.tutor == False:
        if current_user.id != userID:
            return render_template("404.html")

    # Retrieve other relevant information about parent
    familyChildren = Family.query.filter_by(parentID=userID).all() 
    children = [User.query.get(familyChild.studentID) for familyChild in familyChildren]

    # List of tuples of family objects and user objects
    childrenInfo = list(zip(children, familyChildren))

    # Remember that this route was visited
    session['url'] = url_for('parent', userID=userID)

    return render_template("portal-parent.html", parent=parent, children=children, familyChildren=familyChildren, childrenInfo=childrenInfo)

@app.route("/portal/student/<int:userID>")
@login_required
def student(userID):
    """
    Portal for student users. 
    This route gives an overview of all student courses and also provides relevant graphs.
    """

    # Retrieve all test types
    testTypes = TestType.query.all()

    # Retrieve information about student 
    student = User.query.get(userID)

    # Check if the user is actually a student
    if student is None or student.student == False:
        return render_template("404.html")

    # Retrieve other relevant information about student 
    familyParents = Family.query.filter_by(studentID=userID).all()
    parents = [User.query.get(familyParent.parentID) for familyParent in familyParents]

    # List of tuples of family objects and user objects
    parentsInfo = list(zip(parents, familyParents))

    # Retrieving the means of every test type
    typeMeans = TypeMean.query.filter_by(studentID=userID).all() 

    # Get list of id's of parents that are eligible to visit student site 
    eligibleParents = [familyParent.parentID for familyParent in familyParents if familyParent.pending == False]

    # Checking is current user is permitted to visit page
    if current_user.admin == False and current_user.tutor == False:
        if current_user.id != userID:
            if current_user.id not in eligibleParents:
                return render_template("404.html")
    
    # Remember that this route was visited
    session['url'] = url_for('student', userID=userID)
    
    return render_template("portal-student.html", student=student, parents=parents, parentsInfo=parentsInfo, \
        testTypes=testTypes, typeMeans=typeMeans)

@app.route("/portal/<int:userID>/addfamily", methods=["POST"])
@login_required
def addFamily(userID):
    """ Relationship request between children and parents """

    # Check via what page request was made
    submitted = request.form.get("submitted")

    if submitted == "student":
        
        # Retrieve user input
        parentUsername = request.form.get("parent")

        # Checking if that person exists
        parent = User.query.filter_by(username=parentUsername).first()
        if parent is None:
            flash("There is no parent by that username", "warning")
            return redirect(url_for("student", userID=userID))
        
        # Checking if family already exists
        family = Family.query.filter_by(parentID=parent.id, studentID=userID).first()
        if family is not None:
            flash("You already requested a relation with this parent.", "warning")
            return redirect(url_for("student", userID=userID))
        
        # Initiating a new family and adding it to the database
        family = Family(parentID=parent.id, studentID=userID, pending=True, studentSubmit=True, parentSubmit=False)
        db.session.add(family)
        db.session.commit()

        flash("Successfully requested relationship", "success")
        return redirect(url_for("student", userID=userID))
    else:
        
        # Retrieve user input
        studentUsername = request.form.get("student")

        # Checking if that person exists
        student = User.query.filter_by(username=studentUsername).first()
        if student is None:
            flash("There is no student by that username", "warning")
            return redirect(url_for("parent", userID=userID))
        
        # Checking if family already exists
        family = Family.query.filter_by(parentID=userID, studentID=student.id).first()
        if family is not None:
            flash("You already requested a relation with this parent.", "warning")
            return redirect(url_for("parent", userID=userID))

        # Initiating a new family and adding it to the database
        family = Family(parentID=userID, studentID=student.id, pending=True, studentSubmit=False, parentSubmit=True)
        db.session.add(family)
        db.session.commit()

        return redirect(url_for("parent", userID=userID))

@app.route("/portal/pending", methods=["POST"])
@login_required
def pending():
    """ 
    Accepting, Denying a relationship request. 
    Also a route with which you can delete already made requests.
    """

    # Retrieving user input
    decision = request.form.get("decision")
    parentID = request.form.get("parentID")
    studentID = request.form.get("studentID")

    # Retrieving relevant family
    family = Family.query.filter_by(parentID=parentID, studentID=studentID).first()

    # Accepting, denying or deleting the relation
    if decision == "accept":
        family.pending = False
        db.session.commit()
    else: 
        db.session.delete(family)
        db.session.commit()
        
    return redirect(session['url'])

@app.route("/portal/student/<int:userID>/addcourse", methods=["POST"])
@login_required
def addCourse(userID):
    """ Adding courses to a page of a student """

    # Retrieve user input 
    courseName = request.form.get("course")

    # Initiating a new course and adding it to the database 
    course = Course(studentID=userID, name=courseName)
    db.session.add(course)
    db.session.commit()

    return redirect(url_for("student", userID=userID))

@app.route("/portal/student/<int:userID>/course/<int:courseID>")
@login_required
def course(userID, courseID):
    """ Page with grades of the course and also with a graph of how the mean changed over time """

    # Retrieve information about student and course
    student = User.query.get(userID)
    course = Course.query.get(courseID)
    means = CourseMean.query.filter_by(courseID=courseID).all()

    # Check if course exists or if it is actually a course of the student 
    if course is None or course.studentID != userID:
        return render_template("404.html")

    # Retrieve all test types
    testTypes = TestType.query.all()

    return render_template("course.html", student=student, course=course, testTypes=testTypes, means=means)

@app.route("/portal/student/<int:userID>/addgrade", methods=["POST"])
def addGrade(userID):
    """ Route to add grades and calculate the new means """

    # Retrieving date
    today = datetime.now()

    # Retrieving user information
    courseID = request.form.get("course")
    grade = request.form.get("grade")
    weight = request.form.get("weight")
    testTypeID = request.form.get("testType")
    dateTest = request.form.get("dateTest")

    # Initiating new grade object 
    if dateTest == '':
        grade = Grade(courseID=courseID, grade=grade, weight=weight, typeID=testTypeID, date=today, dateUpdate=today)
    else: 
        grade = Grade(courseID=courseID, grade=grade, weight=weight, typeID=testTypeID, date=today, dateUpdate=today, dateTest=dateTest)
    
    # Adding grade to database
    db.session.add(grade)
    db.session.commit()

    # Retrieving all grades from course
    gradeObjects = Grade.query.filter_by(courseID=courseID).all()
    grades = [float(gradeObject.grade) for gradeObject in gradeObjects]
    weights = [float(gradeObject.weight) for gradeObject in gradeObjects]

    # Calculating the (weighted) mean of all grades 
    mean = np.average(grades, weights=weights)

    # Iniating mean object and adding it to database
    meanObject = CourseMean(gradeID=grade.id, courseID=courseID, mean=mean)
    db.session.add(meanObject)
    db.session.commit()

    # Retrieving all grades from user
    courses = Course.query.filter_by(studentID=userID).all()
    typeGradeObjects = []
    for course in courses:
        grades = Grade.query.filter_by(courseID=course.id).all()
        typeGradeObjects += grades 
    
    # Retrieving all test types
    testTypes = TestType.query.all()

    # Calculating the mean for every test type
    for testType in testTypes:
        grades = []
        weights = []
        for typeGradeObject in typeGradeObjects:
            if typeGradeObject.typeID == testType.id:
                grades.append(float(typeGradeObject.grade))
                weights.append(float(typeGradeObject.weight))
                
        if len(grades) > 0:
            mean = np.average(grades, weights=weights)

            # Retrieve old means
            typeMeanObject = TypeMean.query.filter_by(studentID=userID, typeID=testType.id).first()

            # Add new values to database
            if typeMeanObject is None:
                typeMeanObject = TypeMean(studentID=userID, typeID=testType.id, mean=mean)
                db.session.add(typeMeanObject)
            else:
                typeMeanObject.mean = mean
            db.session.commit()

    flash("Succussfully added grade.", "success")
    return redirect(url_for("course", userID=userID, courseID=courseID))

@app.route("/portal/student/<int:userID>/updategrade", methods=["POST"])
def updateGrade(userID):
    """ 
    Route to update already existing grades or even delete them.
    Also the all the means are recalculated. 
    """

    # Retrieving date
    today = datetime.now()

    # Retrieving information and the user decision
    choice = request.form.get("choice")
    gradeID = request.form.get("gradeUpdate")
    grade = Grade.query.get(gradeID)
    courseID = request.form.get("course")
    currentCourse = Course.query.get(courseID)

    # Store updated information in variables
    gradeNew = float(request.form.get("grade"))
    weightNew = float(request.form.get("weight"))
    testTypeIDNew = int(request.form.get("testType"))
    dateTestNew = request.form.get("dateTest")

    # Checking if date of test was filled in 
    if len(dateTestNew) == 0:
        dateTestNew = None

    # Retrieving all courses from user
    courses = Course.query.filter_by(studentID=userID).all()

    # Retrieving all grades from user
    grades = []
    for course in courses:
        grades += Grade.query.filter_by(courseID=course.id).all()

    # Retrieve all test types
    testTypes = TestType.query.all()
    
    # Retrieving means from student: course, type
    courseMeans = CourseMean.query.filter_by(courseID=courseID).all()
    typeMeans = TypeMean.query.filter_by(studentID=userID).all()

    # Sort all the means on date (older to newer)
    courseMeans.sort(key=lambda courseMean: courseMean.grade.date)
        
    # Variables that keep track of the total weight
    courseWeight = 0
    totalWeight = {}
    for testType in testTypes:
        totalWeight[testType.name] = 0     

    # Recalculating all the course means 
    for courseMean in courseMeans:

        # Updating weights 
        courseWeight += courseMean.grade.weight
        totalWeight[courseMean.grade.testType.name] += courseMean.grade.weight 
        
        # If user wants to delete grade
        if choice == "delete":

            # Checking if there is only one grade in the course 
            if len(currentCourse.grades) == 1:
                db.session.delete(courseMean)
                db.session.commit()
            else:
                if courseMean.grade.date == grade.date:
                    db.session.delete(courseMean)
            
            # Redefining the old means
            if courseMean.grade.date > grade.date:
                courseMean.mean = (courseMean.mean * courseWeight -  grade.grade * grade.weight) / (courseWeight - grade.weight) 

        # If user is updating grade
        else: 
            if courseMean.grade.date == grade.date:
                courseMean.mean = (courseMean.mean * courseWeight - grade.grade * grade.weight + gradeNew * weightNew) / (courseWeight - grade.weight + weightNew)

            # Redefining the old means
            elif courseMean.grade.date > grade.date:
                courseMean.mean = (courseMean.mean * courseWeight -  grade.grade * grade.weight + gradeNew * weightNew) / (courseWeight - grade.weight + weightNew) 

    # Recalculating the mean per test type
    for typeMean in typeMeans:
        
        # If user wants to delete grade
        if choice == "delete":

            # Checking if there is only one grade for test type
            if totalWeight[typeMean.testType.name] - grade.weight == 0:
                db.session.delete(typeMean)
            else:
                typeMean.mean = (typeMean.mean * totalWeight[typeMean.testType.name] - grade.grade * grade.weight) / (totalWeight[typeMean.testType.name] - grade.weight)
       
        # If user wants to update grade
        else:
            if typeMean.testType.id == testTypeIDNew:
                typeMean.mean = (typeMean.mean * totalWeight[typeMean.testType.name] - grade.grade * grade.weight + gradeNew * weightNew) / (totalWeight[typeMean.testType.name] - grade.weight + weightNew)
                
            elif typeMean.testType.id == grade.typeID:

                # Checking if there is only one grade for test type
                if totalWeight[typeMean.testType.name] - grade.weight == 0:
                    db.session.delete(typeMean)
                else:
                    typeMean.mean = (typeMean.mean * totalWeight[typeMean.testType.name] + gradeNew * weightNew) / (totalWeight[typeMean.testType.name] + weightNew)   
    
        # Comitting all changes
        db.session.commit()

    # Removing grade
    if choice == "delete":
        db.session.delete(grade)
        flash("Successfully deleted grade", "success")
    else: 
        grade.grade = gradeNew
        grade.weight = weightNew
        grade.typeID = testTypeIDNew
        grade.dateUpdate = today
        grade.dateTest = dateTestNew
        flash("Successfully updated grade", "success")

    # Comitting updated grade    
    db.session.commit()

    return redirect(url_for("course", userID=userID, courseID=courseID))