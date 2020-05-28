from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()


# Class of schools
class School(db.Model):
    __tablename__ = 'schools'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

class SchoolLevel(db.Model):
    __tablename__ = 'schoolLevels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

class SchoolYear(db.Model):
    __tablename__ = 'schoolYears'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)

# Classes that describe user relations
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    key = db.Column(db.LargeBinary, nullable=False)
    salt = db.Column(db.LargeBinary, nullable=False)
    student = db.Column(db.Boolean, nullable=False)
    parent = db.Column(db.Boolean, nullable=False)
    tutor = db.Column(db.Boolean, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    schoolID = db.Column(db.Integer, db.ForeignKey("schools.id"))
    school = db.relationship('School', lazy=True)
    levelID = db.Column(db.Integer, db.ForeignKey("schoolLevels.id"))
    yearID = db.Column(db.Integer, db.ForeignKey("schoolYears.id"))
    courses = db.relationship('Course', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

class Family(db.Model):
    __tablename__ = 'families'
    id = db.Column(db.Integer, primary_key=True)
    parentID = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    studentID = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    pending = db.Column(db.Boolean)
    studentSubmit = db.Column(db.Boolean)
    parentSubmit = db.Column(db.Boolean)

class GroupTime(db.Model):
    __tablename__ = 'groupTimes'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    studentGroups = db.relationship('StudentGroup', backref="group", lazy=True)

    def __repr__(self):
        return f'<Group {self.name} at day {self.day}>'

class StudentGroup(db.Model):
    __tablename__ = 'studentGroups'
    id = db.Column(db.Integer, primary_key=True)
    groupID = db.Column(db.Integer, db.ForeignKey("groupTimes.id"), nullable=False)
    studentID = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    students = db.relationship('User', lazy=True)

# Class that keeps track of student absences 
class StudentAbsent(db.Model):
    __tablename__ = 'studentAbsences'
    id = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    absent = db.Column(db.Boolean, nullable=False)
    permitted = db.Column(db.Boolean, nullable=False)
    late = db.Column(db.Boolean, nullable=False)

# Classes that keep track of performance of students 
class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    grades = db.relationship('Grade', lazy=True)
    means = db.relationship('CourseMean', lazy=True)

    def __repr__(self):
        return '<Course %r>' % self.name

class CourseMean(db.Model):
    __tablename__  = 'courseMeans'
    id = db.Column(db.Integer, primary_key=True)
    gradeID = db.Column(db.Integer, db.ForeignKey('grades.id'), nullable=False)
    grade = db.relationship('Grade', backref="courseMean", lazy=True)
    courseID = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    mean = db.Column(db.Float, nullable=False)

class TypeMean(db.Model):
    __tablename__  = 'typeMeans'
    id = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    typeID = db.Column(db.Integer, db.ForeignKey('testTypes.id'), nullable=False)
    testType = db.relationship('TestType', lazy=True)
    mean = db.Column(db.Float, nullable=False)

class TestType(db.Model):
    __tablename__ = 'testTypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    courseID = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    grade = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    typeID = db.Column(db.Integer, db.ForeignKey("testTypes.id"), nullable=False)
    testType = db.relationship('TestType', lazy=True)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    dateUpdate = db.Column(db.DateTime(timezone=True), nullable=False)
    dateTest = db.Column(db.Date)






