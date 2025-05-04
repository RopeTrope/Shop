from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

class User(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    first_name = database.Column(database.String(256), nullable=False)
    last_name = database.Column(database.String(256), nullable=False)
    email = database.Column(database.String(256), nullable=False, unique=True)
    password = database.Column(database.String(256), nullable=False)
    role = database.Column(database.String(32),nullable=False)

    def __init__(self,firstname,lastname,email,password,role):
        self.first_name = firstname
        self.last_name = lastname
        self.email = email
        self.password = password
        self.role = role
    
    def __repr__(self):
        return f"Name: {self.first_name}, Surname: {self.last_name}, Email: {self.email}, Password: {self.password}"
        