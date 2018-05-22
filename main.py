from flask import Flask, render_template, redirect, url_for, session, request, flash
import os, sqlite3
from utils import api, db

USER_SESSION = "logged_in"

app = Flask(__name__)
app.secret_key = os.urandom(16)

def is_null(username, password, confpw):
    return username == "" or password == "" or confpw == ""

def add_session(username, password):
    if is_null(username, password, "filler"):
            flash("Username or password is blank")
            return False
    if(db.login(username, password)):#if credentials match up in the db...
        session[USER_SESSION] = username
        return True
    else:
        flash("Incorrect login credentials")
        return False

@app.route("/")
def root():
    return render_template("home.html", top_songs = api.get_top_songs(), isLogged = (USER_SESSION in session))

@app.route("/login", methods=["GET", "POST"])
def login():
    if USER_SESSION in session:
        return redirect(url_for("root"))
    elif (request.method == "GET"):
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        if add_session(username, password):
            return redirect(url_for("root"))
        return render_template("login.html")


@app.route("/logout")
def logout():
    if USER_SESSION in session:
		session.pop(USER_SESSION)
    return redirect(url_for("login"))

@app.route("/create", methods=["GET", "POST"])
def create():
    if USER_SESSION in session:
        return redirect(url_for("/"))
    if request.method == "POST":
        print request.form["confirmPassword"]
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirmPassword"]

        if is_null(username, password, confirm_password):
            flash("A field was left empty")
        elif password != confirm_password:
            flash("Password and password confirmation do not match")
        else:
            if not db.create_account(username, password):
                flash("Username taken")
            else:
                return redirect(url_for("login"))
    return render_template("create.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/attendance")
def attendance():
    return render_template("attendance.html")

@app.route("/excuse")
def excuse():
    return render_template("excuse.html")

@app.route("/class")
def classes():
    return render_template("class.html")

@app.route("/student")
def student():
    return render_template("student.html")

if __name__ == "__main__":
    d = sqlite3.connect("data/database.db")
    c = d.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS accounts (username TEXT PRIMARY KEY, password TEXT, favorites TEXT);")
    d.commit()
    app.debug = True
    app.run()
    d.close()
    for f in os.listdir("static"):
        if f[-4:] == ".wav":
            os.remove("static/" + f)
