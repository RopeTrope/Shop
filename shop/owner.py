import os
import time
import requests
from flask import Flask, Response, render_template, request, flash
from flask_jwt_extended import JWTManager, get_jwt_identity
from flask_migrate import Migrate, init, upgrade, migrate, stamp

from models.models import database

from utilities.exceptions import ErrorHandler
from utilities.utilities import check_line,check_extension, file_exist
from utilities.databaseUtils import check_product_exist,add_product, add_category_to_product
from utilities.decorators import owner_required

from config import SPARK_NAME, SPARK_PORT, SPARK_PRODUCT_STATISTICS_ROUTE, SPARK_CATEGORY_STATISTICS_ROUTE

from sqlalchemy.exc import OperationalError

app = Flask(__name__)

app.secret_key = "my-secret-key"

app.config.from_object("config")

jwt = JWTManager(app)

migration = Migrate(app,database)

database.init_app(app)

@app.context_processor
def user_name():
    identity = get_jwt_identity()
    return {"user":identity}



@app.route("/",methods=["GET"])
@owner_required()
def hello_owner():
    return "<h1>Hello owner</h1>"

@app.route("/update", methods=["GET","POST"])
@owner_required()
def update():
    if request.method == "POST":
        file = request.files['file']
        #File is provided
        try:
            file_exist(file)
            #Valid extension of file
            check_extension(file)
        except ErrorHandler as e:
            flash(e.message,"danger")
            return render_template("update.html")

        decoded_file = file.read().decode()
        lines = decoded_file.split('\n')
        for index,line in enumerate(lines): 
            line_split = line.split(',')
            try:
                categories, name, price = check_line(line_split,index).values()    
                product = check_product_exist(name)
                if product:
                    database.session.rollback()
                    raise ErrorHandler(f"Product {name} already exists.",400)
            except ErrorHandler as e:
                flash(e.message, "danger")
                return render_template("update.html")

            product = add_product(name,price)

            categories_splited = categories.split("|")
            for category in categories_splited:
                add_category_to_product(category,product)
        #Commit changes to database
        database.session.commit()
        flash("Products added sucessfully.","success")            
    return render_template("update.html")

@app.route("/product_statistics")
def product_statistics():
    response = requests.get(f"http://{SPARK_NAME}:{SPARK_PORT}/{SPARK_PRODUCT_STATISTICS_ROUTE}")
    return Response(response.text, mimetype="text/html")

@app.route("/category_statistics")
def category_statistics():
    response = requests.get(f"http://{SPARK_NAME}:{SPARK_PORT}/{SPARK_CATEGORY_STATISTICS_ROUTE}")
    return Response(response.text, mimetype="text/html")


migration_path = os.path.join(os.getcwd(),'migrations')
versions_path = os.path.join(migration_path,'versions')

if __name__ == "__main__":
    with app.app_context():
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

    app.run(debug=True,host="0.0.0.0")