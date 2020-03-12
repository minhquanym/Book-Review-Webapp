import os, json

from flask import Flask, render_template, request, redirect

from werkzeug.security import check_password_hash, generate_password_hash

from operator import and_, or_
import requests

from helpers import login_required
from models import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
@login_required
def index():
    """ Show search box """
    return render_template("index.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    """ Log in user """

    # Forget any user_id
    db.session.clear()

    

    # User reached route by submit form
    if request.method == "POST":

        if not request.form.get("username"):
            return render_template("login.html", message="Must provide username")
        if not request.form.get("password"):
            return render_template("login.html", message="Must provide password")

        username = request.form.get("username")
        password = request.form.get("password")
        # Check if username exist and password is correct
        user = User.query.filter(User.username == username).fetchone()
        if user == None or not check_password_hash(user.hash, password):
            return render_template("login.html", message="Invalid username or password")
        # Remember which user has logged in
        db.session["user_id"] = user.id
        db.session["user_name"] = user.username

        # Redirect user to home page
        return redirect("/")
    # User reach by GET
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """ Log user out """

    # Forget any user_id
    db.session.clear()
    # Redirect to home page
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register user """

    # Forget any user_id
    db.session.clear()

    # User reach route by submit form (via POST)
    if request.method == "POST":
        
        if not request.form.get("username"):
            return render_template("register.html", message="Must provide username")
        
        username = request.form.get("username")
        # Check database if username has already existed
        user = User.query.filter(User.username == username).fetchone()
        if user:
            return render_template("register.html", message="Username not available")
        
        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("register.html", message="Must provide password")
        # Ensure confirmation password
        elif not request.form.get("password") == request.form.get("confirmation"):
            return render_template("register.html", message="Password not match")

        # Add user in database
        hashedPassword = generate_password_hash(request.form.get("password"))

        user = User(username=username, hash=hashedPassword)
        db.session().add(user)
        db.session().commit()

