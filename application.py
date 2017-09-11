from flask import Flask, url_for, render_template, session
import sqlalchemy

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")