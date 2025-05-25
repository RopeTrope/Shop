
from models.models import database
from .exceptions import ErrorHandler
import re

from flask_jwt_extended import get_jwt_identity,get_jwt

from flask import make_response, redirect, flash


def get_user_info():
    identity = get_jwt_identity()
    claims = get_jwt()
    user = {
        "email":identity,
        "first_name":claims.get("first_name"),
        "last_name":claims.get("last_name"),
        "role":claims.get("role")
    }
    return user

LOGIN_PAGE = "http://localhost:5000/login"

def file_exist(file):
    if file.filename == "":
        raise ErrorHandler("No file selected. Please add file to update products...",400)

def check_extension(file):
    valid = re.match(r'.+\.csv$',file.filename)
    if not valid:
        raise ErrorHandler("Accepting only files with csv extension.",400)

def check_line_size(line_split,index):
    if len(line_split) != 3:
        database.session.rollback()
        raise  ErrorHandler(f"Incorrect number of values on line {index}",400)

def category_is_empty(categories,index):
    if categories=="":
        database.session.rollback()
        raise ErrorHandler(f"Incorrect number of values on line {index}",400)

def name_is_empty(name,index):
    if name == "":
        database.session.rollback()
        raise ErrorHandler(f"Incorrect number of values on line {index}",400)

def check_price(line_split,index):
    try:
        price = float(line_split[2].strip())
        #Incorrect value for price
        if price <= 0:
            database.session.rollback()
            raise ErrorHandler(f"Incorrect price on line {index}",400)
        return price
    except ValueError as e:
        #Incorrect value for price
        database.session.rollback()
        raise ErrorHandler(f"Incorrect price on line {index}",400) from e
    



def check_line(line_split,index):
    check_line_size(line_split,index)
    categories = line_split[0].strip()
    category_is_empty(categories,index)
    name = line_split[1].strip()
    #Name is empty
    name_is_empty(name,index)
    price = check_price(line_split,index)
    return {"categories":categories,"name":name,"price":price}

def get_email():
    return get_jwt_identity()


def logout_user():
    flash("Your successfully logged out.","success")
    response = make_response(redirect(LOGIN_PAGE))
    response.delete_cookie("access_token_cookie")
    return response


def expired_token():
    flash("Your token has expired please login again.","warning")
    response = make_response(redirect(LOGIN_PAGE))
    response.delete_cookie("access_token_cookie")
    return response

def unauthorized_access():
    flash("You must be logged in to access this page.","warning")
    return redirect(LOGIN_PAGE)

def invalid_token():
    flash("Your token is not valid.","warning")
    return redirect(LOGIN_PAGE)

