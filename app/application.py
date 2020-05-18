import hashlib
import os
import re

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import *

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

# Configuring flask Login
login_manager = LoginManager()
login_manager.init_app(app)

# Method for loading user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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
    return "Test"
