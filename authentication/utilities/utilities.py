from enum import Enum
import re

import bcrypt


class Role(Enum):
    Owner = 1
    Customer = 2
    Courier = 3


def validation(fname,lname,email,password):

    if fname is None or lname is None or email is None or password is None:
        return "One of the fields are missing."
    
    if fname == "":
        return "First name should not be empty."
    
    if lname == "":
        return "Last name should not be empty."
    
    if email == "":
        return "Email should not be empty."
    
    if len(password) <  8:
        return "Invalid password."

    valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
    if not valid:
        return "Email not valid."
    
    return ""

def login_validation(email,password):
    if email == "":
        return "Email is missing."

    if password == "":
        return "Password is missing."
    
    valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
    if not valid:
        return "Email not valid."
    
    return ""

def hashing_password(password):

    bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    return bcrypt.hashpw(bytes,salt)

def check_hash_password(password,hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"),hashed_password.encode("utf-8"))