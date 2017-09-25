from flask import Flask, url_for, render_template, session, request, redirect
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import argon2
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)
app.secret_key = "b\x91\x1a\xc8T\x18\x00\x0f\x8f\xa8\\\xa8\xfe\xb6:\xb3\xcc\xe9\xf8&y\\\xa7-"

class User(db.Model):
    # SQL Alchemy class for users table

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    hashword = db.Column(db.String(120))

    def __init__(self, id, username, hashword):
        self.id = id
        self.username = username
        self.hashword = hashword

class Trucks(db.Model):

    __tablename__ = 'trucks'
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(150))
    destination = db.Column(db.String(150))
    trailer = db.Column(db.String(30))
    comments = db.Column(db.String(200))

    def __init__(self, origin, destination, trailer, comments):
        self.origin = origin
        self.destination = destination
        self.trailer = trailer
        self.comments = comments

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    session.clear()
    error = None

    if request.method == "POST":
        if not request.form.get("username"):
            error = "Username Required"
            return render_template("login.html", error=error)

        elif not request.form.get("password"):
            error = "Password Required"
            return render_template("login.html", error=error)

        userinfo = User.query.filter_by(username=request.form.get("username")).first()

        if userinfo == None or not argon2.verify(request.form.get("password"), userinfo.hashword):
            error = "Invalid username and/or password"
            return render_template("login.html", error=error)

        session["user_id"] = userinfo.id
        return redirect(url_for("index"))

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear()
    return redirect(url_for("login"))

def login_required(f):
    # requires login, from http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/map')
def maps():
    return render_template("map.html")

@app.route('/edittrucks', methods=["GET", "POST"])
@login_required
def edittrucks():

    if request.method == "POST":
        if request.form.get("submit"):
            if not request.form.get("origin") or not request.form.get("destination"):
                error = "Missing origin and/or destination"
                return render_template("edittrucks.html", error=error)

            truckinfo = Trucks(request.form.get("origin"), request.form.get("destination"),
                               request.form.get("trailer"), request.form.get("comments"))

            db.session.add(truckinfo)
            db.session.commit()

            return redirect(url_for("edittrucks"))
        elif request.form.get("delete"):

            truckdelete = Trucks.query.filter_by(id=request.form["delete"]).first()
            db.session.delete(truckdelete)
            db.session.commit()

            return redirect(url_for("edittrucks"))
    trucks = Trucks.query.all()
    return render_template("edittrucks.html", trucks=trucks)