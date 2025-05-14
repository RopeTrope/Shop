from functools import wraps

from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt



def customer_required():
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims["role"] == "Customer":
                return fn(*args, **kwargs)
            else:
                return jsonify({"message":"No permission to access this route.."}), 400
        return decorator
    return wrapper

def owner_required():
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims["role"] == "Owner":
                return fn(*args, **kwargs)
            else:
                return jsonify({"message":"No permission to access this route.."}), 400
        return decorator
    return wrapper

def courier_required():
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims["role"] == "Courier":
                return fn(*args, **kwargs)
            else:
                return jsonify({"message":"No permission to access this route.."}), 400
        return decorator
    return wrapper