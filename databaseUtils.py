from models import User
from models import database
from utilities import hashing_password

def find_user_by_email(email):
   return User.query.filter_by(email=email).first()


def add_user_to_db(fname,lname,email,password,role):
   user = User(fname,lname,email,hashing_password(password),role)
   database.session.add(user)
   database.session.commit()

def delete_user(user):
   database.session.delete(user)
   database.session.commit()