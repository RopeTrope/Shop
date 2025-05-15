from flask import Flask, render_template, request, jsonify

from flask_jwt_extended import JWTManager

from models.models import database

from utilities.utilities import ErrorHandler, get_email

from utilities.databaseUtils import check_product_on_id, get_all_products, add_order,add_order_product,search_categories_on_name, search_products_on_name
from utilities.databaseUtils import get_my_orders, get_products_by_order_id, get_categories_by_product_id, get_quantity, get_my_order_by_id,change_status_of_order
from utilities.decorators import customer_required
from utilities.enums import Status



app = Flask(__name__)

app.config.from_object("config")

jwt = JWTManager(app)

database.init_app(app)


#TODO: Should do the transition to base.html so it looks better and easier
#TODO: Add html
@app.route("/search",methods=["GET","POST"])
@customer_required()
def search():
    if request.method == "POST":
        product_name = request.form.get("pname")
        search_product = "%{}%".format(product_name)
        category_name = request.form.get("category")
        search_category = "%{}%".format(category_name)

        categories = search_categories_on_name(search_category,search_product)
        products = search_products_on_name(search_category, search_product)
        json_products = []
        for product in products:
            json_products.append({"categories":[category.name for category in product.categories],"id":product.id,"name":product.name,"price":product.price})

        return jsonify({"categories":[category.name for category in categories],"products":[product for product in json_products]}),200

    return render_template("search.html")

#TODO: Do the revision of this route
@app.route("/order",methods=["GET","POST"])
@customer_required()
def order():
    products = get_all_products()
    if request.method == "POST":
        product_ids = request.form.getlist('productsId')
        product_quants = request.form.getlist('productsQuant')
        sending_req = []
        try:
            for product_id, product_quant in zip(product_ids,product_quants):
                if int(product_quant) == 0:
                    continue
                if int(product_quant) < 0:
                    raise ErrorHandler("Invalid product quantity.",400)
                
                product_exist = check_product_on_id(product_id)
                if not product_exist:
                    raise ErrorHandler("Invalid product id.",400)
                
                sending_req.append({"id":product_id,"quantity":product_quant})
            
            if sending_req == []:
                raise ErrorHandler("Please pick a product to order.",400)

        except ErrorHandler as e:
            return jsonify({"message":e.message}),e.error_code
        
        order = add_order(get_email(),Status.CREATED.name)
        database.session.commit()

        for x in sending_req:
            add_order_product(order.id,int(x['id']), int(x['quantity']))

        database.session.commit()

        return jsonify({"id":order.id}),200

    return render_template("order.html", products=products)

#TODO: Test when with 2-3 user with different deliveries
#TODO: Adde enums for types of users
@app.route("/status",methods=["GET"])
@customer_required()
def status():
    orders = get_my_orders(get_email())
            
    order_json = []
    products_json = []

    for order in orders:
        products = get_products_by_order_id(order.id)
        price = 0
        for product in products:
            categories = get_categories_by_product_id(product.id)
            quantity = get_quantity(order.id, product.id).quantity
            products_json.append({"categories":[category.name for category in categories], "name":product.name, "price":product.price, "quantity":quantity})
            price += product.price * quantity
        order_json.append({"products":[product_json for product_json in products_json], "price":round(price,2),"status":order.status, "timestamp":order.timestamp})
        products_json = []

    return render_template("status.html",orders=order_json)
            

@app.route("/delivered", methods=["GET","POST"])
@customer_required()
def delivered():
    orders = get_my_orders(get_email())
    if request.method == "POST":
        order_id = request.form.get("orderId")
        try:
            if order_id is None:
                raise ErrorHandler("Order id is missing",400)
            
            order_exists = get_my_order_by_id(order_id,get_email())

            if not order_exists:
                raise ErrorHandler("Order with this id does not exists.",400)        
            
            if order_exists.status == Status.COMPLETED.name:
                raise ErrorHandler("Order is already completed.",400)


        except ErrorHandler as e:
            return jsonify({"message":e.message}),e.error_code
    
        change_status_of_order(order_exists,Status.COMPLETED.name)

    return render_template("delivered.html",orders=orders)


#TODO: Continue now to delivery
if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0")