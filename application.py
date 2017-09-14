from flask import Flask, url_for, render_template, session, request, redirect
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)
app.secret_key = "b\x91\x1a\xc8T\x18\x00\x0f\x8f\xa8\\\xa8\xfe\xb6:\xb3\xcc\xe9\xf8&y\\\xa7-"

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    hashword = db.Column(db.String(120))

    def __init__(self, id, username, hashword):
        self.id = id
        self.username = username
        self.hashword = hashword

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
        if userinfo == None or not pwd_context.verify(request.form.get("password"), userinfo.hashword):
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

@app.route('/map')
def maps():
    return render_template("map.html")