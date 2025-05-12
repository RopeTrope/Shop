
from models.models import database
from .exceptions import ErrorHandler
import re

from flask_jwt_extended import get_jwt_identity


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