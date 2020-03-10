import os

from flask import Flask, render_template, request
from models import *


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

curUser = -1
@app.route("/")
def index():
    if curUser != -1:
        return render_template("welcome.html")
    return render_template("index.html")

@app.route("/login")
def login():
    if curUser != -1:
        return render_template("welcome.html")
    return render_template("login.html")

@app.route("/register")
def register():
    if curUser != -1:
        return render_template("welcome.html")
    return render_template("register.html")