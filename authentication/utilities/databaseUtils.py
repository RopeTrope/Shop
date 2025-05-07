from models.models import User
from models.models import database
from utilities.utilities import hashing_password
import json

def find_user_by_email(email):
   return User.query.filter_by(email=email).first()


def add_user_to_db(fname,lname,email,password,role):
   user = User(fname,lname,email,hashing_password(password),role)
   database.session.add(user)
   database.session.commit()

def delete_user(user):
   database.session.delete(user)
   database.session.commit()

def create_owners():
   with open("owner.json","r") as file:
      data = json.load(file)
      owners = data["owners"]

      for owner in owners:
         fname = owner["first_name"]
         lname = owner["last_name"]
         mail = owner["email"]
         password = owner["password"]
         role = "Owner"
         user_exists = find_user_by_email(mail)
         if user_exists is None:
            add_user_to_db(fname,lname,mail,password,role)
   print("All owners are created")

      