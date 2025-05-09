from flask import Flask, render_template, request, jsonify
from models.models import database
from utilities.exceptions import ErrorHandler
from utilities.utilities import check_line,check_extension, file_exist
from utilities.databaseUtils import check_product_exist,add_product, add_category_to_product


import re

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

database.init_app(app)

#TODO: Need to add JWT access control 
@app.route("/",methods=["GET"])
def hello_owner():
    return "<h1>Hello owner</h1>"

#TODO: Maybe add message when csv file is added successfully
#TODO: Make it one try except
#TODO: Refactor it a lil bit more later
@app.route("/update", methods=["GET","POST"])
def update():
    if request.method == "POST":
        file = request.files['file']
        #File is provided
        try:
            file_exist(file)
        except ErrorHandler as e:
            return jsonify({"message":e.message}),e.error_code
        
        #Valid extension of file
        try:
            check_extension(file)
        except ErrorHandler as e:
            return jsonify({"message":e.message}),e.error_code

        decoded_file = file.read().decode()
        lines = decoded_file.split('\n')
        for index,line in enumerate(lines): 
            line_split = line.split(',')
            try:
                categories, name, price = check_line(line_split,index).values()
            except ErrorHandler as e:
                return jsonify({"message":e.message}),e.error_code
            
            try:
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



#TODO: inserting to test the database
#Database was created good i guess
if __name__ == "__main__":
    with app.app_context():
        database.create_all()
    app.run(debug=True,port=5100)