import sqlite3, hashlib
import os

DIR = os.path.dirname(__file__)
DIR += '/'
m = DIR + "../data/database.db"

# Login - Returns true if successful, false otherwise
def login(username, password):
    print "THIS IS M " + m
    db = sqlite3.connect(m)
    c = db.cursor()
    c.execute("SELECT username, password FROM profiles WHERE username = '%s';" % (username));
    for account in c:
        user = account[0]
        passw = account[1]
        # Check if user and encrypted password match
        print username + " " + user
        print passw + " " + encrypt_password(password)
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
    db.commit()
    db.close()
    return False

# Checks if username exists - Returns true if username exists, false otherwise
def does_username_exist(username):
    db = sqlite3.connect(m)
    c = db.cursor()
    c.execute("SELECT username FROM profiles WHERE username = '%s';" % (username))
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
    db.commit()
    db.close()
    return False

# Returns full name of a specific user - else returns False if failed
def get_name(username):
    db = sqlite3.connect(m)
    c = db.cursor()
    if does_username_exist(username):
        c.execute("SELECT fullname FROM profiles WHERE username = '%s';" % (username))
        for account in c:
            db.commit()
            db.close()
            return account[0]
    print "Username does not exist"
    db.commit()
    db.close()
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
    db.commit()
    db.close()
    return False

# Returns a list of leaders of a specific course - else Returns False if failed
def get_leaders(coursecode):
    db = sqlite3.connect(m)
    c = db.cursor()
    if does_course_exist(coursecode):
        c.execute("SELECT leader FROM leaders WHERE coursecode = '%s';" % (coursecode))
        leaders = []
        for course in c:
            leaders.append(course[0])
        print "Leaders Returned: " + str(leaders)
        db.commit()
        db.close()
        return leaders
    print "Course does not exist"
    db.commit()
    db.close()
    return False

# Returns a list of students enrolled in a specific course - else Returns False if failed
def get_students(coursecode):
    db = sqlite3.connect(m)
    c = db.cursor()
    if does_course_exist(coursecode):
        c.execute("SELECT student FROM enrollment WHERE coursecode = '%s';" % (coursecode))
        students = []
        for student in c:
            students.append(student[0])
        print "Students Returned: " + str(students)
        db.commit()
        db.close()
        return students
    print "Course does not exist"
    db.commit()
    db.close()
    return False

# Authorizes student into the class
def authorize_class(coursecode, password):
    db = sqlite3.connect(m)
    c = db.cursor()
    c.execute("SELECT coursecode, password FROM classes WHERE coursecode = '%s';" % (coursecode));
    for course in c:
        ccode = course[0]
        passw = course[1]
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
        c.execute("INSERT INTO attendance VALUES('%s', '%s', '%s', 'U', '');" % (username, day, course))
        print "Attendance added"
        db.commit()
        db.close()
        return True
    db.commit()
    db.close()
    print "Attendance didn't work"
    return False

# Returns whether or not the class exists
def does_course_exist(coursecode):
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
def create_class(teacher, coursecode, password):
    db = sqlite3.connect(m)
    c = db.cursor()
    if not does_course_exist(coursecode):
        # Add course to classes table
        c.execute("INSERT INTO classes VALUES('%s', '%s', '%s');" % (teacher, coursecode, encrypt_password(password)))
        db.commit()
        db.close()
        print "Create Course Successful"
        return True
    print "Create Course Failed"
    db.commit()
    db.close()
    return False

# Gets all the available classes
def get_classes(username):
    db = sqlite3.connect(m)
    c = db.cursor()
    if get_account(username) == 'T':
        c.execute("SELECT coursecode FROM classes WHERE teacher='%s';" %(username))
        classes = []
        for course in c:
            classes.append(course[0])
    if get_account(username) == 'L':
        c.execute("SELECT coursecode FROM leaders WHERE leader='%s';" %(username))
        classes = []
        for course in c:
            classes.append(course[0])
    print "Classes Returned: " + str(classes)
    db.commit()
    db.close()
    return classes

# Adds leader to the class - Returns true if successful or false if not
def add_leader(coursecode, username):
    db = sqlite3.connect(m)
    c = db.cursor()
    if does_course_exist(coursecode) and does_username_exist(username):
        # Add leader to leaders table
        c.execute("INSERT INTO leaders VALUES('%s', '%s');" % (coursecode, username))
        c.execute("UPDATE profiles SET account='L' WHERE username='%s';" %(username))
        db.commit()
        db.close()
        print "Add Leader Successful"
        return True
    print "add Leader Failed"
    db.commit()
    db.close()
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
    db.commit()
    db.close()
    return False

# Adds student to the class - Returns true if successful or false if not
def add_student(coursecode, username, fullname):
    db = sqlite3.connect(m)
    c = db.cursor()
    if does_course_exist(coursecode) and does_username_exist(username):
        # Add student to enrollment table
        print '2'
        c.execute("INSERT INTO enrollment VALUES('%s', '%s', '%s', NULL);" % (coursecode, username, fullname))
        db.commit()
        db.close()
        print "Add Student Successful"
        return True
    print "Add Student Failed"
    db.commit()
    db.close()
    return False

# Removes student from the class - Returns true if successful or false if not
def remove_student(coursecode, username):
    db = sqlite3.connect(m)
    c = db.cursor()
    if does_course_exist(coursecode) and does_username_exist(username):
        # Add student to enrollment table
        c.execute("DELETE FROM enrollment WHERE coursecode = '%s' AND student = '%s';" % (coursecode, username))
        db.commit()
        db.close()
        print "Deleted Student Successful"
        return True
    print "Deleted Student Failed"
    db.commit()
    db.close()
    return False

# Get grade for student in class - Returns the value
def get_grade(coursecode, username):
    db = sqlite3.connect(m)
    c = db.cursor()
    if does_course_exist(coursecode) and does_username_exist(username):
        c.execute("SELECT grade FROM enrollment WHERE coursecode = '%s' AND student = '%s';" % (coursecode, username))
        for grade in c:
            print "Grade Returned: " + str(grade)
            db.commit()
            db.close()
            return grade[0]
    db.commit()
    db.close()
    return 'not yet inputted'

# Changes grade for student in class - Returns true if successful or false if not
def change_grade(coursecode, username, grade):
    db = sqlite3.connect(m)
    c = db.cursor()
    if does_course_exist(coursecode) and does_username_exist(username):
        remove_student(coursecode, username)
        c.execute("INSERT INTO enrollment VALUES('%s', '%s', '%s', %d);" % (coursecode, username, get_name(username), grade))
        db.commit()
        db.close()
        print "Changed Grade Successful"
        return True
    print "Changed Grade Failed"
    db.commit()
    db.close()
    return False

# Counts number of unexcused absences for a student
def count_unexcused(username):
    db = sqlite3.connect(m)
    c = db.cursor()
    ans = 0
    if does_username_exist(username):
        c.execute("SELECT type FROM attendance WHERE username = '%s' AND type = 'U';" % (username))
        for grade in c:
            ans += 1
        print "Unexcused: " + str(ans)
    db.commit()
    db.close()
    return ans

# Counts number of excused absences for a student
def count_excused(username):
    db = sqlite3.connect(m)
    c = db.cursor()
    ans = 0
    if does_username_exist(username):
        c.execute("SELECT type FROM attendance WHERE username = '%s' AND type = 'E';" % (username))
        for grade in c:
            ans += 1
        print "Unexcused: " + str(ans)
    db.commit()
    db.close()
    return ans

# Gets all the classes that a student is enrolled in
def get_studentclass(username):
    db = sqlite3.connect(m)
    c = db.cursor()
    c.execute("SELECT coursecode FROM enrollment WHERE student = '%s';" %(username))
    classes = []
    for course in c:
        classes.append(course[0])
    print "Classes Returned: " + str(classes)
    db.commit()
    db.close()
    return classes

# Checks if student was present on a given day for a given course - Returns true if absent, false if not
def student_present(username, date, course):
    db = sqlite3.connect(m)
    c = db.cursor()
    if does_course_exist(course) and does_username_exist(username):
        c.execute("SELECT type FROM attendance WHERE username='%s' AND day='%s' AND course='%s';" % (username, date, course))
        for account in c:
            db.commit()
            db.close()
            print "Absent"
            return False
    print "Present"
    db.commit()
    db.close()
    return True

# Checks if student was absent on a given day for a given course - Returns true if absent, false if not
def check_attendance(username, date, course):
    db = sqlite3.connect(m)
    c = db.cursor()
    if does_course_exist(course) and does_username_exist(username):
        c.execute("SELECT type FROM attendance WHERE username='%s' AND day='%s' AND course='%s';" % (username, date, course))
        for account in c:
            db.commit()
            db.close()
            print "Absence recorded"
            return False
    print "No absence recorded"
    db.commit()
    db.close()
    return True

# Removes attendance for those marked present - Returns true if removed, false if not
def delete_attendance(username, date, course):
    db = sqlite3.connect(m)
    c = db.cursor()
    if does_course_exist(course) and does_username_exist(username):
        c.execute("DELETE FROM attendance WHERE username='%s' AND day='%s' AND course='%s';" % (username, date, course))
        db.commit()
        db.close()
        print "Absence removed"
        return False
    print "No absence removed"
    db.commit()
    db.close()
    return True
