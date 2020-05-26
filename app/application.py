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
admin.add_view(ModelView(Family, db.session))
admin.add_view(ModelView(GroupTime, db.session))
admin.add_view(ModelView(StudentGroup, db.session))
admin.add_view(ModelView(StudentAbsent, db.session))
admin.add_view(ModelView(Course, db.session))
admin.add_view(ModelView(TestType, db.session))
admin.add_view(ModelView(Grade, db.session))

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
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/testimonials")
def testimonials():
    return render_template("testimonials.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


# User registration
@app.route("/signup", methods=["GET", "POST"])
def signup():

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
        student = False
        parent = False 
        if role == "student":
            student = True
        elif role == "parent":
            parent = True 
            school = None
            schoolLevel = None
            schoolYear = None

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

        return "Yello"

    return render_template("signup.html", schools = schools, schoolLevels = schoolLevels, schoolYears = schoolYears)

# Routes that are used for signup validation
@app.route("/usernamecheck", methods=["POST"])
def usernamecheck():

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

    # Retrieving password
    password = request.form.get("password")
    password_repeat = request.form.get("password_repeat")

    # Checking if password satisfies the requirements
    if pass_validation(password)[0] == False:
        return jsonify({"password_success": False, "message": pass_validation(password)[1]})
    else:
        return jsonify({"password_success": True, "message": pass_validation(password)[1]})

@app.route("/passwordcrossvalidation", methods=["POST"])
def passwordcrossvalidation():

    # Retrieving password information
    password = request.form.get("password")
    password_repeat = request.form.get("password_repeat")

    if password != password_repeat:
        return jsonify({"password_success": False, "message": "The passwords do not match!"})
    else:
        return jsonify({"password_success": True, "message": "Looks good!"})

@app.route("/emailcheck", methods=["POST"])
def emailcheck():

    email = request.form.get("email")
    user = User.query.filter_by(email=email).first()
    if user is not None:
        email_available = False
        return jsonify({"email_available": False, "message": "This e-mail is already in use."})
    else:
        return jsonify({"email_available": True})

@app.route("/login", methods=["GET", "POST"])
def login():

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
            elif user.parent or user.tutor:
                return redirect(url_for("all"))
            else:
                return redirect(url_for("student"))


    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/portal")
@login_required
def portal():

    # Retrieve all users
    users = User.query.all()

    return render_template("portal.html", users=users)

@app.route("/portal/tutor")
@login_required
def tutor():
    students = User.query.filter_by(student=True).all()
    groups = GroupTime.query.all()
    return render_template("portal-tutor.html", students=students, groups=groups)

@app.route("/portal/parent/<int:userID>")
def parent(userID):

    # Retrieve information about parent
    parent = User.query.filter_by(id=userID).first()
    familyChildren = Family.query.filter_by(parentID=userID).all() 
    children = [User.query.get(familyChild.studentID) for familyChild in familyChildren]
    childrenInfo = zip(children, familyChildren)

    # Remember that this route was visited
    session['url'] = url_for('parent', userID=userID)

    return render_template("portal-parent.html", parent=parent, children=children, familyChildren=familyChildren, childrenInfo=childrenInfo)

@app.route("/portal/student/<int:userID>")
@login_required
def student(userID):

    # Retrieve all test types
    testTypes = TestType.query.all()

    # Retrieve information about student 
    student = User.query.filter_by(id=userID).first()
    familyParents = Family.query.filter_by(studentID=userID).all()
    parents = [User.query.get(familyParent.parentID) for familyParent in familyParents]
    parentsInfo = zip(parents, familyParents)
    overallMeans = OverallMean.query.filter_by(studentID=userID) 

    # Remember that this route was visited
    session['url'] = url_for('student', userID=userID)
    
    return render_template("portal-student.html", student=student, parents=parents, parentsInfo=parentsInfo, testTypes=testTypes, overallMeans=overallMeans)

@app.route("/portal/<int:userID>/addfamily", methods=["POST"])
@login_required
def addFamily(userID):

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

    decision = request.form.get("decision")
    parentID = request.form.get("parentID")
    studentID = request.form.get("studentID")

    if decision == "accept":
        family = Family.query.filter_by(parentID=parentID, studentID=studentID).first()
        family.pending = False
        db.session.commit()
    else: 
        family = Family.query.filter_by(parentID=parentID, studentID=studentID).first()
        db.session.delete(family)
        db.session.commit()
        
    return redirect(session['url'])


@app.route("/portal/student/<int:userID>/addcourse", methods=["POST"])
@login_required
def addCourse(userID):

    # Retrieve user input 
    courseName = request.form.get("course")

    # Initiating a new course and adding it to the database 
    course = Course(studentID=int(userID), name=courseName)
    db.session.add(course)
    db.session.commit()

    return redirect(url_for("student", userID=userID))

@app.route("/portal/student/<int:userID>/course/<int:courseID>")
@login_required
def course(userID, courseID):

    # Retrieve information about student and course
    student = User.query.filter_by(id=userID).first()
    course = Course.query.filter_by(id=courseID).first()
    means = Mean.query.filter_by(courseID=courseID).all()

    # Retrieve all test types
    testTypes = TestType.query.all()

    # Retrieve information about course 
    return render_template("course.html", student=student, course=course, testTypes=testTypes, means=means)

@app.route("/portal/student/<int:userID>/addgrade", methods=["POST"])
def addGrade(userID):
    
    # Retrieving date
    today = datetime.now()

    # Retrieving user information
    courseName = request.form.get("course")
    grade = request.form.get("grade")
    weight = request.form.get("weight")
    testTypeID = request.form.get("testType")
    dateTest = request.form.get("dateTest")

    # Retrieving course id
    course = Course.query.filter_by(studentID=userID, name=courseName).first()
    courseID = course.id

    # Initiating new grade object 
    if dateTest == '':
        grade = Grade(courseID=courseID, grade=grade, weight=weight, typeID=testTypeID, dateAdded=today, dateUpdate=today)
    else: 
        grade = Grade(courseID=courseID, grade=grade, weight=weight, typeID=testTypeID, dateAdded=today, dateUpdate=today, dateTest=dateTest)
    
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
    meanObject = Mean(courseID=courseID, mean=mean, date=today)
    db.session.add(meanObject)
    db.session.commit()

    # Retrieving all grades from user
    courses = Course.query.filter_by(studentID=userID).all()
    overallGradeObjects = []
    for course in courses:
        grades = Grade.query.filter_by(courseID=course.id).all()
        overallGradeObjects += grades 
    
    # Retrieving all test types
    testTypes = TestType.query.all()

    # Calculating the mean for every test type
    for testType in testTypes:
        grades = []
        weights = []
        for overallGradeObject in overallGradeObjects:
            if overallGradeObject.typeID == testType.id:
                grades.append(float(overallGradeObject.grade))
                weights.append(float(overallGradeObject.weight))
            
        mean = np.average(grades, weights=weights)
        overallMeanObject = OverallMean(studentID=userID, typeID=testType.id, mean=mean, date=today)
        db.session.add(overallMeanObject)
        db.session.commit()

    return redirect(url_for("course", userID=userID, courseID=courseID))

