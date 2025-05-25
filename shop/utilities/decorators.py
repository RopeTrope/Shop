from functools import wraps

from flask import flash, redirect
from flask_jwt_extended import jwt_required, get_jwt
from .enums import Role
from .utilities import LOGIN_PAGE





def customer_required():
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims["role"] == Role.Customer.name:
                return fn(*args, **kwargs)
            else:
                flash("No permission to access this route.","warning")
                return redirect(LOGIN_PAGE)
        return decorator
    return wrapper

def owner_required():
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims["role"] == Role.Owner.name:
                return fn(*args, **kwargs)
            else:
                flash("No permission to access this route.","warning")
                return redirect(LOGIN_PAGE)
        return decorator
    return wrapper

def courier_required():
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims["role"] == Role.Courier.name:
                return fn(*args, **kwargs)
            else:
                flash("No permission to access this route.","warning")
                return redirect(LOGIN_PAGE)
        return decorator
    return wrapper