import time
from flask import Flask, render_template, request, jsonify, redirect, make_response
from sqlalchemy.exc import OperationalError
from models.models import database
from utilities.utilities import validation,login_validation,check_hash_password
from utilities.databaseUtils import find_user_by_email,add_user_to_db,delete_user
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_jwt_extended import set_access_cookies

from flask_migrate import Migrate



app = Flask(__name__)

app.config.from_object("config")

jwt = JWTManager(app)

#Added migration for database
migrate = Migrate(app,database)

#initialize database
database.init_app(app)
migrate.init_app(app,database)

@app.route("/",methods=['GET'])
def hello():
    return render_template("index.html")

@app.route("/hello",methods=['GET'])
@jwt_required()
def forbidden():
    ident = get_jwt_identity()
    return f"Hello {ident} to forbidden page"

#TODO: Change login.html href so it can go to either customer register or register courier
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
            return jsonify({"message":error}),400
        user_exists = find_user_by_email(email)
        if user_exists is not None:
            return jsonify({"message": "Email already exists."}),400
        
        add_user_to_db(fname,lname,email,password,"Customer")

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
            return jsonify({"message":error}),400
        
        user_exists = find_user_by_email(email)
        
        if user_exists is not None:
            return jsonify({"message":"Email already exists."}),400
        
        add_user_to_db(fname,lname,email,password,"Courier")

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
            return jsonify({"message":error}),400

        user_exists = find_user_by_email(email)
        if user_exists is None:
            return jsonify({"message":"Invalid credentials."}),400
        else:
            if check_hash_password(password,user_exists.password) is False:
                return jsonify({"message":"Invalid credentials."}),400

        #TODO: Bad practice to return hashed_password but for now it can stay
        claims = {
            "first_name":user_exists.first_name,
            "last_name":user_exists.last_name,
            "password":user_exists.password,
            "role":user_exists.role
                   }
        token = create_access_token(identity=email, additional_claims=claims)
        response = make_response(redirect("/hello"))
        set_access_cookies(response,token)
        return response
    
    return render_template("login.html")


@app.route("/delete",methods=["POST"])
@jwt_required()
def delete():
    identity = get_jwt_identity()

    user_exists = find_user_by_email(identity)

    if user_exists is None:
        return jsonify({"message": "Unknown user."}),400
    
    response = make_response(redirect("/login"))
    response.delete_cookie("access_token_cookie")
    delete_user(user=user_exists)

    return response


@jwt.expired_token_loader
def handle_expired_token(jwt_header,jwt_payload):
    #If any of tokens are expired force login this is the easiest way
    #Maybe it can be done if refresh token expired force login
    #But if it is access put a page where you have to click to refresh token
    #Which send post to /refresh_token
    response = make_response(redirect("/login"))
    response.delete_cookie("access_token_cookie")
    return response

#TODO: Password for mysql should be moved, maybe using environment variables
#TODO: Maybe it can be added to auto migrate
if __name__ == "__main__":
    with app.app_context():
        #creating orm database
        created = False
        while created is False:
            try:
                database.create_all()
                created = True
            except OperationalError:
                time.sleep(3) 
    app.run(debug=True, host="0.0.0.0")
