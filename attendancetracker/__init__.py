from flask import Flask, render_template, redirect, url_for, session, request, flash, Markup
import os, sqlite3, datetime, calendar
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
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if USER_SESSION in session:
        accttype = db.get_account(USER_SESSION)
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
        accttype = db.get_account(USER_SESSION)
        if accttype == 'S':
            return redirect(url_for("profile"))
        if accttype == 'L':
            return redirect(url_for("attendance"))
        return redirect(url_for("home"))
    if request.method == "POST":
        print request.form["confirmPassword"]
        username = request.form["username"]
        fullname = request.form["fullname"]
        accttype = request.form["accttype"]
        password = request.form["password"]
        confirm_password = request.form["confirmPassword"]

        if not username.endswith("@stuy.edu"):
            flash("Email must be your stuy.edu email")
        elif is_null(username, password, confirm_password):
            flash("A field was left empty")
        elif password != confirm_password:
            flash("Password and password confirmation do not match")
        else:
            if not db.create_account(username, password, fullname, accttype):
                flash("Username taken")
            else:
                return redirect(url_for("login"))
    return render_template("create.html", isLogged = (USER_SESSION in session))

@app.route("/profile")
def profile():
    if not USER_SESSION in session:
        return redirect(url_for("login"))
    else:
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        WDFOM = datetime.date(year, month, 1).weekday() # what weekday the first day of month is
        bmonth = month - 1  # how many days in the month before  and calculating the previous month
        byear = year
        if bmonth < 1:  # Accounting for the wrapping around
            byear -= 1
            bmonth += 12
        amonth = month + 1  # Calculating the next month
        ayear = year
        if amonth > 12:  # Accounting for the wrapping around
            ayear += 1
            amonth -= 12
        WDFLM = calendar.monthrange(byear, (bmonth))[1]
        numinmonth = calendar.monthrange(year, (month))[1] # how many days in current month
        monthTable = []
        pre = (WDFOM + 1) % 7  # Number of days of the previous month
        while pre > 0:
            monthTable.append(WDFLM - pre)  # Add those days in
            pre -= 1
        cur = 1
        while cur <= numinmonth:  # Adding in the days in the current month
            monthTable.append(cur)
            cur += 1
        nex = 1
        while len(monthTable) % 7 > 0:  # Adding in days until the calendar ends on Saturday
            monthTable.append(nex)
            nex += 1
        def maketable(test):  # Makes the table
            final = "<table border='1'>\n"
            final += "<tr> <th> Sunday </th> \
        <th> Monday </th> <th> Tuesday </th> <th> Wednesday </th> \
        <th> Thursday </th> <th> Friday </th> <th> Saturday </th> </tr>\n"
            for x in range(len(test)):
                if x % 7 == 0:
                    final += '<tr>'
                final += '<td>' + str(test[x]) + '</td>'
                if x % 7 == 6:
                    final += '</tr>\n'
            final += '</table>'
            return final
        monthString = Markup("<strong>" + "<h1>" + calendar.month_name[month] + ", " + str(year) + "</h1>" + maketable(monthTable) + "</strong>")
        print monthString
        return render_template("profile.html", user=USER_SESSION, month=monthString, isLogged = (USER_SESSION in session))


@app.route("/home")
def home():
    if not USER_SESSION in session:
        return redirect(url_for("login"))
    else:
        accttype = db.get_account(USER_SESSION)
        if accttype == 'S':
            return redirect(url_for("profile"))
        if accttype == 'L':
            return redirect(url_for("attendance"))
        return render_template("home.html", isLogged = (USER_SESSION in session))

@app.route("/attendance")
def attendance():
    if not USER_SESSION in session:
        return redirect(url_for("login"))
    else:
        if accttype == 'S':
            return redirect(url_for("profile"))
        if accttype == 'T':
            return redirect(url_for("home"))
        return render_template("attendance.html", date="10/07/2017", course="UVS11-01", isLogged = (USER_SESSION in session))

@app.route("/excuse")
def excuse():
    if not USER_SESSION in session:
        return redirect(url_for("login"))
    else:
        if accttype == 'S':
            return redirect(url_for("profile"))
        return render_template("excuse.html", name="Giorgio Vidali", user="gvidali@stuy.edu", isLogged = (USER_SESSION in session))

@app.route("/class")
def classes():
    if not USER_SESSION in session:
        return redirect(url_for("login"))
    else:
        if accttype == 'S':
            return redirect(url_for("profile"))
        if accttype == 'L':
            return redirect(url_for("attendance"))
        return render_template("class.html", isLogged = (USER_SESSION in session))

@app.route("/student")
def student():
    if not USER_SESSION in session:
        return redirect(url_for("login"))
    else:
        if accttype == 'S':
            return redirect(url_for("profile"))
        if accttype == 'L':
            return redirect(url_for("attendance"))
        return render_template("student.html", name="Kevin Li", user="kli16@stuy.edu", grade="99", isLogged = (USER_SESSION in session))

if __name__ == "__main__":
    DIR = os.path.dirname(__file__)
    DIR += ‘/’
    DATA = DIR + "data/database.db"
    d = sqlite3.connect(DATA)
    c = d.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS profiles (username TEXT PRIMARY KEY, password TEXT, fullname TEXT, account TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS attendance (username TEXT, day TEXT, type TEXT, reason TEXT);")
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
