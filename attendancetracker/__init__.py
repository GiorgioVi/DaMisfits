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
        elif accttype == 'T':
            if admin_password == "":
                flash("To create a teacher account, please enter admin password")
            elif admin_password and db.encrypt_password(admin_password) != 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb':
                flash("Admin password is incorrect")
        elif not db.create_account(username, password, fullname, accttype):
            flash("Username taken")
        else:
            return redirect(url_for("login"))

    return render_template("create.html", isLogged = (USER_SESSION in session))


@app.route("/profile", methods=["GET","POST"])
def profile():
    if not USER_SESSION in session:
        return redirect(url_for("login"))

    user = session[USER_SESSION]
    accttype = db.get_account(user)
    fullname = db.get_name(user)
    if accttype == 'T':
        return redirect(url_for("home"))

    if request.method == "POST":
        coursecode = request.form['classcode']
        password = request.form['password']
        if db.authorize_class(coursecode, password):
            db.add_student(coursecode, user, fullname)
            flash("Enrolled in class!")
        else:
            flash("Invalid credentials for class")

    unexcused = db.count_unexcused(user)
    excused = db.count_excused(user)
    info = [unexcused, excused]

    enrolled = {}
    for each in db.get_studentclass(user):
        enrolled[each] = db.get_grade(each, user)

    return render_template("profile.html", attendance=info, enrolled=enrolled, username=user, fullname=fullname, isLogged = (USER_SESSION in session), acct = accttype)


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
        #today = str(date.today())
        print 'request.form'
        print request.form

    #search
    if request.method == "GET" and 'date' in request.args:
        date = request.args.get("date")
        course = request.args.get("course")
        enrolled = db.get_students(course)
        students = {}
        for each in enrolled:
            students[each] = [db.get_name(each), db.student_present(each, date, course)]

        return render_template("attendance.html", date=date, students=students, course=course, courses=classes, isLogged=(USER_SESSION in session), searched=True, acct = accttype)

    return render_template("attendance.html", courses=classes, isLogged=(USER_SESSION in session), acct = accttype)


@app.route("/excuse", methods=["GET","POST"])
def excuse():
    if not USER_SESSION in session:
        return redirect(url_for("login"))

    user = session[USER_SESSION]
    accttype = db.get_account(user)
    if accttype == 'S':
        return redirect(url_for("profile"))

    classes = db.get_classes()
    if request.method == "POST":
        date = request.form["date"]
        reason = request.form["reason"]
        person = request.form["name"]
        course = request.args.get("course")
        db.add_attendance(person, date, course, 'E', reason)
    if request.method == "GET" and 'course' in request.args:
        course = request.args.get("course")
        if not 'student' in request.args:
            students = db.get_students(course)
            return render_template("excuse.html", students=students, course=course, courses=classes, isLogged=(USER_SESSION in session), acct = accttype)
        else:
            return render_template("excuse.html", course=course, courses=classes, isLogged=(USER_SESSION in session), searched=True, acct = accttype)

    return render_template("excuse.html", courses=classes, isLogged = (USER_SESSION in session), acct = accttype)


@app.route("/class", methods=["GET","POST"])
def classes():
    if not USER_SESSION in session:
        return redirect(url_for("login"))

    user = session[USER_SESSION]
    accttype = db.get_account(user)
    if accttype == 'S':
        return redirect(url_for("profile"))

    if request.method == "POST":
        code = request.form["newCode"]
        password = request.form["newPassword"]
        confirm_password = request.form["repeatPassword"]
        classtype = request.form["accttype"]
        if '-' not in code:
            flash("Code must include section")
        elif is_null(code, classtype, password, confirm_password):
            flash("A field was left empty")
        elif password != confirm_password:
            flash("Password and password confirmation do not match")
        elif not db.create_class(user, code, password, classtype):
            flash("Course code taken")
        flash("Course Created!")

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

    classes = db.get_classes()
    if request.method == "POST":
        grade = request.form["grade"]
        person = request.form["name"]
        course = request.args.get("course")
        db.add_grade(course, person, grade)
    if request.method == "GET" and 'course' in request.args:
        course = request.args.get("course")
        if not 'student' in request.args:
            students = db.get_students(course)
            return render_template("student.html", students=students, course=course, courses=classes, isLogged=(USER_SESSION in session), acct = accttype)
        else:
            return render_template("student.html", course=course, courses=classes, isLogged=(USER_SESSION in session), searched=True, acct = accttype)

    return render_template("student.html", name="Kevin Li", user="kli16@stuy.edu", grade="99", isLogged = (USER_SESSION in session), acct = accttype)


if __name__ == "__main__":
    d = sqlite3.connect("data/database.db")
    c = d.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS profiles (username TEXT PRIMARY KEY, password TEXT, fullname TEXT, account TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS attendance (username TEXT, day TEXT, course TEXT, type TEXT, reason TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS classes (teacher TEXT, coursecode TEXT PRIMARY KEY, password TEXT, type TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS leaders (coursecode TEXT, leader TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS enrollment (coursecode TEXT, student TEXT, name TEXT);")
    db.create_account('t@stuy.edu','a', 'Teacher Demo', 'T')
    db.create_account('l@stuy.edu','a', 'Leader Demo', 'L')
    db.create_account('s@stuy.edu','a', 'Student Demo', 'S')
    d.commit()
    app.debug = True
    app.run()
    d.close()
    for f in os.listdir("static"):
        if f[-4:] == ".wav":
            os.remove("static/" + f)
