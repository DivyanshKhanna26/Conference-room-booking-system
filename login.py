from database import conn, cursor
import hashlib
from organization_administrator import org_admin_actions
from administrator import administrator_actions


def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()


def login():
    print("Log In:")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    hashed_password = hash_password(password)
    cursor.execute("SELECT * FROM Users WHERE email = ? AND password = ?", (email, hashed_password))
    user = cursor.fetchone()
    if user:
        org_id = user[1]
        org_name = ""
        if(org_id != 0):
            cursor.execute("SELECT org_name FROM Organizations WHERE org_id = ?", (user[1],))
            org_name = cursor.fetchone()
        print("Login successful!")
        print(f"Welcome, {user[2]}!")
        if org_name:
            print(f"Organization: {org_name[0]}")

        if user[5] == 'org_admin':
            org_admin_actions(user)
        
        elif user[5] == 'Administrator':
            administrator_actions(user)
    else:
        print("Invalid credentials. Please try again.")
