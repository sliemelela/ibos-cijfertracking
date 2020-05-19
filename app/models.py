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

# Class of users
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
    levelID = db.Column(db.Integer, db.ForeignKey("schoolLevels.id"))
    yearID = db.Column(db.Integer, db.ForeignKey("schoolYears.id"))