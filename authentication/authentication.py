from flask import Flask, render_template, request, redirect, make_response,flash

from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_jwt_extended import set_access_cookies

from flask_migrate import Migrate, init, upgrade, migrate, stamp

from sqlalchemy.exc import OperationalError
from models.models import database

from utilities.utilities import validation, login_validation, check_hash_password, Role
from utilities.databaseUtils import find_user_by_email, add_user_to_db, delete_user, create_owners
import os
import time




app = Flask(__name__)
#TODO: Move this
app.secret_key = "my-secret-key"
app.config.from_object("config")
jwt = JWTManager(app)
migration = Migrate(app,database)
database.init_app(app)
migration.init_app(app,database)

@app.route("/",methods=['GET'])
def hello():
    return render_template("index.html")

@app.route("/hello",methods=['GET'])
@jwt_required()
def forbidden():
    ident = get_jwt_identity()
    return f"Hello {ident} to forbidden page"

@app.route("/register_customer",methods=["GET","POST"])
def register_customer():
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("mail")
        password = request.form.get("pass")
        data = {"fname":fname,"lname":lname,"email":email,"password":password}
        error = validation(**data)
        if error != "":
            flash(error,"danger")
            return render_template("register_customer.html")
        user_exists = find_user_by_email(email)
        if user_exists is not None:
            flash("Email already exists","danger")
            return render_template("register_customer.html")
        
        add_user_to_db(fname,lname,email,password,Role.Customer.name)
        flash("You successfully created new account. Now you can login.","success")

        return redirect("/login")

    return render_template("register_customer.html")

@app.route("/register_courier",methods=["GET","POST"])
def register_courier():
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("mail")
        password = request.form.get("pass")

        data = {"fname":fname,"lname":lname,"email":email,"password":password}
        error = validation(**data)

        if error != "":
            flash(error,"danger")
            return render_template("register_courier.html")
        
        user_exists = find_user_by_email(email)
        
        if user_exists is not None:
            flash("Email already exists","danger")
            return render_template("register_courier.html")
        
        add_user_to_db(fname,lname,email,password,Role.Courier.name)
        flash("You successfully created new account. Now you can login.","success")
        return  redirect("/login")

    return render_template("register_courier.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("mail")
        password = request.form.get("pass")
        data = {"email": email, "password":password}

        error = login_validation(**data)

        if error != "":
            flash(error,"danger")
            return render_template("login.html")

        user_exists = find_user_by_email(email)
        if user_exists is None:
            flash("Invalid credentials","danger")
            return render_template("login.html")
        else:
            if check_hash_password(password,user_exists.password) is False:
                flash("Invalid credentials","danger")
                return render_template("login.html")

        claims = {
            "first_name":user_exists.first_name,
            "last_name":user_exists.last_name,
            "role":user_exists.role
                   }
        token = create_access_token(identity=email, additional_claims=claims)
        response = make_response(redirect("/hello"))
        set_access_cookies(response,token)
        return response
    
    return render_template("login.html")


@app.route("/delete",methods=["GET","POST"])
@jwt_required()
def delete():
    if request.method == "POST":
        identity = get_jwt_identity()
        user_exists = find_user_by_email(identity)
        if user_exists is None:
            flash("Unknown user.","danger")
            return render_template("delete.html")
        response = make_response(redirect("/login"))
        response.delete_cookie("access_token_cookie")
        delete_user(user=user_exists)
        flash("User deleted successfully.","success")
        return response
    return render_template("delete.html")


@jwt.expired_token_loader
def handle_expired_token(jwt_header,jwt_payload):
    flash("Your token has expired please login again.","warning")
    response = make_response(redirect("/login"))
    response.delete_cookie("access_token_cookie")
    return response

@jwt.invalid_token_loader
def handle_invalid_token(reason):
    flash("Your token is not valid.","warning")
    return redirect("/login")


@jwt.unauthorized_loader
def unauthorized_error(reason):
    flash("You must be logged in to access this page.","warning")
    return redirect("/login")


migration_path = os.path.join(os.getcwd(),'migrations')
versions_path = os.path.join(migration_path,'versions')

def create_db_and_run_migrations():
    with app.app_context():
        #creating orm database
        created = False
        while created is False:
            try:
                database.create_all()
                created = True
            except OperationalError:
                time.sleep(3) 

        if not os.path.exists(versions_path):
            init(directory=migration_path,multidb=False)
            stamp(directory=migration_path, revision='head')
        migrate(directory=migration_path, message="Initial migration")
        upgrade(directory=migration_path)
        create_owners()

#TODO: Add logout
#TODO: Add home for all types of users html
if __name__ == "__main__":
    create_db_and_run_migrations()
    app.run(debug=True, host="0.0.0.0")
