from flask import Flask, render_template, request, jsonify
from models.models import database, Category, Product


import re

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

database.init_app(app)

#TODO: Need to add JWT access control 
@app.route("/",methods=["GET"])
def hello_owner():
    return "<h1>Hello owner</h1>"

#TODO: Make it readable
#TODO: Maybe add message when csv file is added successfully
@app.route("/update", methods=["GET","POST"])
def update():
    if request.method == "POST":
        file = request.files['file']
        #File is provided
        if file.filename == "":
            return jsonify({"message":"No file selected. Please add file to update products..."}),400
        
        #Valid extension of file
        valid = re.match(r'.+\.csv$',file.filename)
        if not valid:
            return jsonify({"message":"Accepting only files with csv extension."}),400

        #TODO: Move to another place
        decoded_file = file.read().decode()
        lines = decoded_file.split('\n')
        for index,line in enumerate(lines): 
            line_split = line.split(',')
            #Number of values in line
            if len(line_split) != 3:
                database.session.rollback()
                return jsonify({"message":f"Incorrect number of values on line {index}"}),400
            categories = line_split[0].strip()
            #Category is empty
            if categories=="":
                database.session.rollback()
                return jsonify({"message":f"Incorrect number of values on line {index}"}),400
            name = line_split[1].strip()
            #Name is empty
            if name == "":
                database.session.rollback()
                return jsonify({"message":f"Incorrect number of values on line {index}"}),400
            try:
                price = float(line_split[2].strip())
                #Incorrect value for price
                if price <= 0:
                    database.session.rollback()
                    return jsonify({"message":f"Incorrect price on line {index}"}),400
            except ValueError:
                #Incorrect value for price
                database.session.rollback()
                return jsonify({"message":f"Incorrect price on line {index}"}),400
            

            #Product already exists
            product_exists = Product.query.filter_by(name=name).first()
            if product_exists:
                database.session.rollback()
                return jsonify({"message":f"Product {name} already exists."}),400
            product = Product(name,price)
            database.session.add(product)
            #TODO:Check if two same categories are sent or just delete duplicates if there are same in sam line
            #If category already exists do not add but use existing instead
            categories_splited = categories.split("|")
            for category in categories_splited:
                print(category)
                category_exists = Category.query.filter_by(name=category).first()
                if not category_exists:
                    category = Category(category)
                    product.categories.append(category)
                else:
                    product.categories.append(category_exists)

        #Commit changes to database
        database.session.commit()            

    return render_template("update.html")



#TODO: inserting to test the database
#Database was created good i guess
if __name__ == "__main__":
    with app.app_context():
        database.create_all()
    app.run(debug=True,port=5100)