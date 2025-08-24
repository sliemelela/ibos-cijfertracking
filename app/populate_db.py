# This script populates the database so that the web app is functional. 
import os, hashlib, getpass

## Create admin account
while True:
    password0 = getpass.getpass("Set admin password: ")
    password1 = getpass.getpass("Confirm password: ")
    if password0 == password1:
        print("Passwords match!\n")
        break
    else:
        print("Passwords do not match! Please retry.\n")

salt = os.urandom(32)
key = hashlib.pbkdf2_hmac('sha256', password0.encode("utf-8"), salt, 100000)
user = User(
    username = "admin", 
    firstName = "Admin", 
    lastName = "Admin", 
    email = "admin@ibos.nu", 
    key = key, 
    salt = salt,
    student = False, 
    parent = False, 
    tutor = False, 
    admin = True
    )

db.session.add(user)
db.session.commit()
print("Successfully created admin user.")

## Create school
school = School(
    name = "tmp"
    )

db.session.add(school)
db.session.commit()
print("Successfully created tmp school.")

## Create school level
schoolLevel = SchoolLevel(
    name = "tmp"
    )

db.session.add(schoolLevel)
db.session.commit()
print("Successfully created tmp school level.")

## Create school year
schoolYear = SchoolYear(
    year = 1
    )

db.session.add(schoolYear)
db.session.commit()
print("Successfully created 1 school year.")

## Create test type
testType = TestType(
    name = "tmp"
    )

db.session.add(testType)
db.session.commit()
print("Successfully created tmp test type.")

exit()