import os

from flask import Flask, render_template, request
from models import *
from operator import and_


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

curUserId = -1
@app.route("/")
def index():
    if curUserId != -1:
        return render_template("welcome.html", curUserId)
    return render_template("index.html", message="")

@app.route("/login", methods = ["POST"])
def login():
    # Login to your account
    if curUserId != -1:
        return render_template("welcome.html", curUserId)
    username = request.form.get("username")
    password = request.form.get("password")
    
    user = User.query.filter(and_(User.username == username, User.password == password)).first()
    if not user:
        return render_template("index.html", message="Your username or password is wrong")

    return render_template("login.html")

@app.route("/register")
def register():
    if curUserId != -1:
        return render_template("welcome.html", curUserId)
    return render_template("register.html")