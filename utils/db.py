import sqlite3, hashlib

m = "data/database.db"

# Login - Returns true if successful, false otherwise
def login(username, password):
    db = sqlite3.connect(m)
    c = db.cursor()
    c.execute("SELECT username, password FROM accounts WHERE username = '%s'" % (username));
    for account in c:
        user = account[0]
        passw = account[1]
        # Check if user and encrypted password match
        if username == user and encrypt_password(password) == passw:
            print "Successful Login"
            return True
    print "Login Failed"
    return False

# Encrypt password - SHA256
def encrypt_password(password):
    encrypted = hashlib.sha256(password).hexdigest()
    return encrypted

# Create account - Returns true if successful, false otherwise
def create_account(username, password):
    db = sqlite3.connect(m)
    c = db.cursor()
    if not does_username_exist(username):
        # Add user to accounts table
        c.execute("INSERT INTO accounts VALUES('%s', '%s', '[]')" % (username, encrypt_password(password)))
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
    c.execute("SELECT username FROM accounts WHERE username = '%s'" % (username))
    for account in c:
        # Username exists
        print "Username exists"
        return True
    print "Username does not exist"
    return False

if __name__ == '__main__':
    m = "../data/database.db"
    db = sqlite3.connect(m)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS accounts (username TEXT PRIMARY KEY, password TEXT, favorites TEXT);")
    db.commit()
    create_account("jxu10@stuy.edu", "ibm135")
    create_account("gvidali@stuy.edu", "shrek")
    create_account("kli16@stuy.edu", "p455w0rd3")
    db.close()
