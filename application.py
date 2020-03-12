import os, json

from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

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

# Configure session to use filesystem
app.secret_key = "dit me deo hieu sao can secret key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
db.init_app(app)


@app.route("/")
@login_required
def index():
    """ Show search box """
    books = Book.query.limit(15).all()
    return render_template("index.html", books=books)

@app.route("/login", methods = ["GET", "POST"])
def login():
    """ Log in user """

    # Forget any user_id
    session.clear()

    # User reached route by submit form
    if request.method == "POST":

        if not request.form.get("username"):
            return render_template("login.html", message="Must provide username")
        if not request.form.get("password"):
            return render_template("login.html", message="Must provide password")

        username = request.form.get("username")
        password = request.form.get("password") 
        # Check if username exist and password is correct
        user = User.query.filter(User.username == username).first()
        if user == None or not check_password_hash(user.hash, password):
            return render_template("login.html", message="Invalid username or password")
        # Remember which user has logged in
        session["user_id"] = user.id
        session["user_name"] = user.username

        # Redirect user to home page
        return redirect("/")
    # User reach by GET
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """ Log user out """

    # Forget any user_id
    session.clear()
    # Redirect to home page
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register user """

    # Forget any user_id
    session.clear()

    # User reach route by submit form (via POST)
    if request.method == "POST":
        
        if not request.form.get("username"):
            return render_template("register.html", message="Must provide username")
        
        username = request.form.get("username")
        # Check database if username has already existed
        user = User.query.filter(User.username == username).first()
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
        
        # flash('Account created', 'info')
        
        return redirect("/login")

    # User reach via GET
    else:
        return render_template("register.html")

@app.route("/search", methods=["GET"])
@login_required
def search():
    """ Get book search results """

    # Take input 
    query = "%" + request.args.get("search") + "%"

    books = Book.query.filter(or_(Book.isbn.like(query), or_(Book.title.like(query), Book.author.like(query)))).limit(15).all()

    if not books:
        return render_template("index.html", books = books, message="No book match your description")
    else:
        return render_template("index.html", books = books, message="Result search for '" + request.args.get("search") + "':")

@app.route("/book/<isbn>", methods=["GET", "POST"])
@login_required
def book(isbn):
    """Save and show user reviews"""

    if request.method == "POST":
        # Get info of current user
        curUserId = session["user_id"]
        user = User.query.get(curUserId) 

        comment = request.form.get("comment")

        book = Book.query.filter(Book.isbn == isbn).first()
        book.add_comment(text=comment, username=user.username)

        return redirect("/book/" + book.isbn)
    else:
        book = Book.query.filter(Book.isbn == isbn).first()
        comments = book.comments
        return render_template("book.html", book=book, comments=comments)
        