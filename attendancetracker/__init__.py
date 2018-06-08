from flask import Flask, render_template, redirect, url_for, session, request, flash, Markup
import os, sqlite3, datetime, calendar
from utils import api, db
from datetime import date


USER_SESSION = "logged_in"

app = Flask(__name__)
app.secret_key = os.urandom(16)

def is_null(username, fullname, password, confpw):
    return username == "" or fullname == "" or password == "" or confpw == ""

def add_session(username, password):
    if is_null(username, password, "filler", "filler"):
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
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if USER_SESSION in session:
        user = session[USER_SESSION]
        accttype = db.get_account(user)
        if accttype == 'S':
            return redirect(url_for("profile"))
        if accttype == 'L':
            return redirect(url_for("attendance"))
        return redirect(url_for("home"))
    elif (request.method == "GET"):
        return render_template("login.html", isLogged = (USER_SESSION in session))
    else:
        username = request.form["username"]
        password = request.form["password"]
        if add_session(username, password):
            return redirect(url_for("root"))
    return render_template("login.html", isLogged = (USER_SESSION in session))


@app.route("/logout")
def logout():
    if USER_SESSION in session:
		session.pop(USER_SESSION)
    return redirect(url_for("login"))


@app.route("/create", methods=["GET", "POST"])
def create():
    if USER_SESSION in session:
        user = session[USER_SESSION]
        accttype = db.get_account(user)
        if accttype == 'S':
            return redirect(url_for("profile"))
        if accttype == 'L':
            return redirect(url_for("attendance"))
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form["username"]
        fullname = request.form["fullname"]
        accttype = request.form["accttype"]
        password = request.form["password"]
        confirm_password = request.form["confirmPassword"]
        admin_password = request.form["adminPassword"]

        if not username.endswith("@stuy.edu"):
            flash("Email must be your stuy.edu email")
        elif is_null(username, fullname, password, confirm_password):
            flash("A field was left empty")
        elif password != confirm_password:
            flash("Password and password confirmation do not match")
        elif not db.create_account(username, password, fullname, accttype):
            flash("Username taken")
        elif accttype == 'T':
            if admin_password == "":
                flash("To create a teacher account, please enter admin password")
            elif admin_password and db.encrypt_password(admin_password) != 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb':
                flash("Admin password is incorrect")
        else:
            return redirect(url_for("login"))

    return render_template("create.html", isLogged = (USER_SESSION in session))


@app.route("/profile")
def profile():
    if not USER_SESSION in session:
        return redirect(url_for("login"))

    user = session[USER_SESSION]
    accttype = db.get_account(user)
    if accttype == 'T':
        return redirect(url_for("home"))

    return render_template("profile.html", username=user, isLogged = (USER_SESSION in session), acct = accttype)


@app.route("/home", methods=["GET","POST"])
def home():
    if not USER_SESSION in session:
        return redirect(url_for("login"))

    user = session[USER_SESSION]
    accttype = db.get_account(user)
    if accttype == 'S':
        return redirect(url_for("profile"))
    if accttype == 'L':
        return redirect(url_for("attendance"))

    return render_template("home.html", isLogged = (USER_SESSION in session), acct = accttype)


@app.route("/attendance", methods=["GET","POST"])
def attendance():
    if not USER_SESSION in session:
        return redirect(url_for("login"))

    user = session[USER_SESSION]
    accttype = db.get_account(user)
    if accttype == 'S':
        return redirect(url_for("profile"))

    classes = db.get_classes()
    #coming back from excuse
    if request.method == "POST":
        today = str(date.today())
        return render_template("attendance.html", date=today, course=course, courses=classes, isLogged=(USER_SESSION in session), acct = accttype)
    #search
    if request.method == "GET" and 'date' in request.args:
        date = request.args["date"]
        course = request.args["course"]
        return render_template("attendance.html", date=date, course=course, courses=classes, isLogged=(USER_SESSION in session), searched=True, acct = accttype)

    return render_template("attendance.html", courses=classes, isLogged=(USER_SESSION in session), acct = accttype)


@app.route("/excuse", methods=["GET","POST"])
def excuse():
    if not USER_SESSION in session:
        return redirect(url_for("login"))

    user = session[USER_SESSION]
    accttype = db.get_account(user)
    if accttype == 'S':
        return redirect(url_for("profile"))

    if request.method == "POST":
        date = request.form["date"]
        reason = request.form["reason"]
        person = request.form["name"]
        course = request.args["course"]
        db.add_attendance(person, date, course, 'E', reason)
        return redirect(url_for("attendance"))

    return render_template("excuse.html", name="Giorgio Vidali", username="gvidali@stuy.edu", isLogged = (USER_SESSION in session), acct = accttype)


@app.route("/class", methods=["GET","POST"])
def classes():
    if not USER_SESSION in session:
        return redirect(url_for("login"))

    user = session[USER_SESSION]
    accttype = db.get_account(user)
    if accttype == 'S':
        return redirect(url_for("profile"))

    return render_template("class.html", isLogged = (USER_SESSION in session), acct = accttype)


@app.route("/student", methods=["GET","POST"])
def student():
    if not USER_SESSION in session:
        return redirect(url_for("login"))

    user = session[USER_SESSION]
    accttype = db.get_account(user)
    if accttype == 'S':
        return redirect(url_for("profile"))
    if accttype == 'L':
        return redirect(url_for("attendance"))

    return render_template("student.html", name="Kevin Li", user="kli16@stuy.edu", grade="99", isLogged = (USER_SESSION in session), acct = accttype)


if __name__ == "__main__":
    d = sqlite3.connect("data/database.db")
    c = d.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS profiles (username TEXT PRIMARY KEY, password TEXT, fullname TEXT, account TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS attendance (username TEXT, day TEXT, course TEXT, type TEXT, reason TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS classes (teacher TEXT, coursecode TEXT PRIMARY KEY, password, TEXT, type TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS leaders (coursecode TEXT, leader TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS enrollment (coursecode TEXT, student TEXT);")
    d.commit()
    app.debug = True
    app.run()
    d.close()
    for f in os.listdir("static"):
        if f[-4:] == ".wav":
            os.remove("static/" + f)
