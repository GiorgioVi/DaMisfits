import sqlite3, hashlib
import os

DIR = os.path.dirname(__file__)
DIR += '/'
m = DIR + "../data/database.db"

# Login - Returns true if successful, false otherwise
def login(username, password):
    print "THIS IS M" + m
    db = sqlite3.connect(m)
    c = db.cursor()
    c.execute("SELECT username, password FROM profiles WHERE username = '%s';" % (username));
    for account in c:
        user = account[0]
        passw = account[1]
        # Check if user and encrypted password match
        if username == user and encrypt_password(password) == passw:
            print "Successful Login"
            db.commit()
            db.close()
            return True
    print "Login Failed"
    db.commit()
    db.close()
    return False

# Encrypt password - SHA256
def encrypt_password(password):
    encrypted = hashlib.sha256(password).hexdigest()
    return encrypted

# Create account - Returns true if successful, false otherwise
def create_account(username, password, fullname, account):
    db = sqlite3.connect(m)
    c = db.cursor()
    if not does_username_exist(username):
        # Add user to profiles table
        c.execute("INSERT INTO profiles VALUES('%s', '%s', '%s', '%s');" % (username, encrypt_password(password), fullname, account))
        db.commit()
        db.close()
        print "Create Account Successful"
        return True
    print "Create Account Failed"
    return False

# Checks if username exists - Returns true if username exists, false otherwise
def does_username_exist(username):
    db = sqlite3.connect(m)
    c = db.cursor()
    c.execute("SELECT username FROM profiles WHERE username = '%s';" % (username))
    print c
    for account in c:
        # Username exists
        print "Username exists"
        db.commit()
        db.close()
        return True
    print "Username does not exist"
    db.commit()
    db.close()
    return False

# Returns account type of a specific user - else returns False if failed
def get_account(username):
    db = sqlite3.connect(m)
    c = db.cursor()
    if does_username_exist(username):
        c.execute("SELECT account FROM profiles WHERE username = '%s';" % (username))
        for account in c:
            db.commit()
            db.close()
            return account[0]
    print "Username does not exist"
    return False

# Returns class type of a specific course - else Returns False if failed
def get_classtype(coursecode):
    db = sqlite3.connect(m)
    c = db.cursor()
    if not does_course_exist(coursecode):
        c.execute("SELECT type FROM classes WHERE coursecode = '%s';" % (coursecode))
        for course in c:
            print "Class Type Returned: " + str(course)
            db.commit()
            db.close()
            return course[0]
    print "Course does not exist"
    return False

# Returns a list of leaders of a specific course - else Returns False if failed
def get_leaders(coursecode):
    db = sqlite3.connect(m)
    c = db.cursor()
    if not does_course_exist(coursecode):
        c.execute("SELECT leader FROM leaders WHERE coursecode = '%s';" % (coursecode))
        leaders = []
        for course in c:
            leaders.append(course)
        print "Leaders Returned: " + str(leaders)
        db.commit()
        db.close()
        return leaders
    print "Course does not exist"
    return False

# Returns a list of students enrolled in a specific course - else Returns False if failed
def get_students(coursecode):
    db = sqlite3.connect(m)
    c = db.cursor()
    if not does_course_exist(coursecode):
        c.execute("SELECT student FROM enrollment WHERE coursecode = '%s';" % (coursecode))
        students = []
        for student in c:
            students.append(student)
        print "Students Returned: " + str(students)
        db.commit()
        db.close()
        return students
    print "Course does not exist"
    return False

# Authorizes student into the class
def authorize_class(coursecode, password):
    db = sqlite3.connect(m)
    c = db.cursor()
    c.execute("SELECT coursecode, password FROM classes WHERE coursecode = '%s';" % (coursecode));
    for course in c:
        ccode = account[0]
        passw = account[1]
        # Check if ccode and encrypted password match
        if coursecode == ccode and encrypt_password(password) == passw:
            print "Successful Authorization Into Class"
            db.commit()
            db.close()
            return True
    print "Class Authorization Failed"
    db.commit()
    db.close()
    return False

# Adds unexcused attendance if DNE, else excuses with reason
def add_attendance(username, course, day, type, reason):
    db = sqlite3.connect(m)
    c = db.cursor()

    if type == 'E':
        c.execute("UPDATE attendance SET type = 'E', reason = '%s' WHERE username = '%s' AND day = '%s' AND course = '%s';" % (reason, username, day, course))
        print "Attendance updated to excused"
        db.commit()
        db.close()
        return True
    else:
        c.execute("INSERT INTO attendance VALUES('%s', '%s', '%s', 'U');" % (username, day, course))
        print "Attendance added"
        db.commit()
        db.close()
        return True

    print "Attendance didn't work"
    return False

# Returns whether or not the class exists
def does_class_exit(coursecode):
    db = sqlite3.connect(m)
    c = db.cursor()
    c.execute("SELECT coursecode FROM classes WHERE coursecode = '%s';" % (coursecode))
    for course in c:
        # course exists
        print "Course exists"
        db.commit()
        db.close()
        return True
    print "Course does not exist"
    db.commit()
    db.close()
    return False

# Creates class if class does not exist - Returns true if successful or false if not
def create_class(teacher, coursecode, password, type):
    db = sqlite3.connect(m)
    c = db.cursor()
    if not does_course_exist(coursecode):
        # Add course to classes table
        c.execute("INSERT INTO classes VALUES('%s', '%s', '%s', '%s');" % (teacher, coursecode, encrypt_password(password), type))
        db.commit()
        db.close()
        print "Create Course Successful"
        return True
    print "Create Course Failed"
    return False

# Gets all the available classes
def get_classes():
    db = sqlite3.connect(m)
    c = db.cursor()
    c.execute("SELECT * FROM classes;")
    classes = []
    for course in c:
        classes.append(course)
    print "Classes Returned: " + str(classes)
    db.commit()
    db.close()
    return classes

# Adds leader to the class - Returns true if successful or false if not
def add_leader(coursecode, username):
    db = sqlite3.connect(m)
    c = db.cursor()
    if not does_course_exist(coursecode) and not does_username_exist(username):
        # Add leader to leaders table
        c.execute("INSERT INTO leaders VALUES('%s', '%s');" % (coursecode, username))
        db.commit()
        db.close()
        print "Add Leader Successful"
        return True
    print "add Leader Failed"
    return False

# Removes leader from the class - Returns true if successful or false if not
def remove_leader(coursecode, username):
    db = sqlite3.connect(m)
    c = db.cursor()
    if not does_course_exist(coursecode) and not does_username_exist(username):
        # Add leader to leaders table
        c.execute("DELETE FROM leaders WHERE coursecode = '%s' AND username = '%s';" % (coursecode, username))
        db.commit()
        db.close()
        print "Deleted Leader Successful"
        return True
    print "Deleted Leader Failed"
    return False

# Adds student to the class - Returns true if successful or false if not
def add_student(coursecode, username, fullname):
    db = sqlite3.connect(m)
    c = db.cursor()
    if not does_course_exist(coursecode) and not does_username_exist(username):
        # Add student to enrollment table
        c.execute("INSERT INTO enrollment VALUES('%s', '%s', '%s');" % (coursecode, username, fullname))
        db.commit()
        db.close()
        print "Add Leader Successful"
        return True
    print "add Leader Failed"
    return False

# Removes student from the class - Returns true if successful or false if not
def remove_student(coursecode, username):
    db = sqlite3.connect(m)
    c = db.cursor()
    if not does_course_exist(coursecode) and not does_username_exist(username):
        # Add student to enrollment table
        c.execute("DELETE FROM enrollment WHERE coursecode = '%s' AND username = '%s';" % (coursecode, username))
        db.commit()
        db.close()
        print "Deleted Student Successful"
        return True
    print "Deleted Student Failed"
    return False



# Get grade for student in class - Returns the value
def get_grade(coursecode, username):
    db = sqlite3.connect(m)
    c = db.cursor()
    if not does_course_exist(coursecode) and not does_username_exist(username):
        c.execute("SELECT grade FROM profiles WHERE coursecode = '%s' AND username = '%s';" % (coursecode, username))
        for grade in c:
            print "Grade Returned: " + str(grade)
            db.commit()
            db.close()
            return grade[0]
        return True
    print "Receive Grade Failed"
    return False

# Changes grade for student in class - Returns true if successful or false if not
def change_grade(coursecode, username, grade):
    db = sqlite3.connect(m)
    c = db.cursor()
    if not does_course_exist(coursecode) and not does_username_exist(username):
        c.execute("UPDATE profiles SET grade=%d;" % (grade))
        db.commit()
        db.close()
        print "Changed Grade Successful"
        return True
    print "Changed Grade Failed"
    return False

if __name__ == '__main__':
    m = "../data/database.db"
    db = sqlite3.connect(m)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS profiles (username TEXT PRIMARY KEY, password TEXT, fullname TEXT, account TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS attendance (username TEXT, day TEXT, course TEXT, type TEXT, reason TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS classes (teacher TEXT, coursecode TEXT PRIMARY KEY, password, TEXT, type TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS leaders (coursecode TEXT, leader TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS enrollment (coursecode TEXT, student TEXT, name TEXT, grade INT);")
    db.commit()
    create_account("jxu10@stuy.edu", "ibm135")
    create_account("gvidali@stuy.edu", "shrek")
    create_account("kli16@stuy.edu", "p455w0rd3")
    db.close()
