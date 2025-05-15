import os
import time

from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate, init, upgrade, migrate, stamp

from models.models import database

from utilities.exceptions import ErrorHandler
from utilities.utilities import check_line,check_extension, file_exist
from utilities.databaseUtils import check_product_exist,add_product, add_category_to_product
from utilities.decorators import owner_required

from sqlalchemy.exc import OperationalError

app = Flask(__name__)

app.config.from_object("config")

jwt = JWTManager(app)

migration = Migrate(app,database)

database.init_app(app)

@app.route("/",methods=["GET"])
@owner_required()
def hello_owner():
    return "<h1>Hello owner</h1>"

#TODO: Maybe add message when csv file is added successfully
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
            return jsonify({"message":e.message}),e.error_code

        decoded_file = file.read().decode()
        lines = decoded_file.split('\n')
        for index,line in enumerate(lines): 
            line_split = line.split(',')
            try:
                categories, name, price = check_line(line_split,index).values()    
                product = check_product_exist(name)
            except ErrorHandler as e:
                return jsonify({"message":e.message}),e.error_code

            product = add_product(name,price)

            categories_splited = categories.split("|")
            for category in categories_splited:
                add_category_to_product(category,product)
        #Commit changes to database
        database.session.commit()            
    return render_template("update.html")


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