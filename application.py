import os

from flask import Flask, render_template, request
# from flask_login import LoginManager
from models import *
from operator import and_, or_

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


# login_manager = LoginManager()
# login_manager.init_app(app)
curUserId = -1

@app.route("/")
def index():
    if curUserId != -1:
        return render_template("welcome.html")
    return render_template("index.html", message="")

@app.route("/login", methods = ["POST"])
def login():
    # Login to your account
    global curUserId
    if curUserId != -1:
        return render_template("welcome.html")
    username = request.form.get("username")
    password = request.form.get("password")
    
    user = User.query.filter(and_(User.username == username, User.password == password)).first()
    if not user:
        return render_template("index.html", message="Your username or password is wrong")
    curUserId = user.id
    return render_template("welcome.html")

@app.route("/register")
def register():
    global curUserId
    if curUserId != -1:
        return render_template("welcome.html")
    return render_template("register.html", message="")

@app.route("/logout")
def logout():
    curUserId = -1
    return render_template("index.html", message="")

@app.route("/newuser", methods = ["POST"])
def newuser():
    username = request.form.get("username")
    password = request.form.get("password")
    password2 = request.form.get("password2")
    
    if password != password2:
        return render_template("register.html", message="Confirm password not match")
    
    exists = db.session.query(db.session.query(User).filter_by(username=username).exists()).scalar()

    if exists == True:
        return render_template("register.html", message="Username not available")

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return render_template("index.html", message="You registered completely. Lets login to review books")
    
@app.route('/search', methods = ["POST", "GET"])
def search():
    text = request.form.get("search")
    books = Book.query.limit(30).all()
    return render_template("welcome.html", books=books)

@app.route("/book/<int:book_id>")
def book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return render_template("welcome.html")
    return render_template("book.html", book=book)
