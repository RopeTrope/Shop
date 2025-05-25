from flask import Flask, render_template, request,flash 
from flask_jwt_extended import JWTManager, get_jwt_identity

from models.models import database

from utilities.utilities import ErrorHandler, get_email, get_user_info, expired_token, unauthorized_access, invalid_token, logout_user

from utilities.databaseUtils import check_product_on_id, get_all_products, add_order,add_order_product,search_categories_on_name, search_products_on_name, update_product_waiting
from utilities.databaseUtils import get_my_orders, get_products_by_order_id, get_categories_by_product_id, get_quantity, get_my_order_by_id,change_status_of_order, update_product_sold
from utilities.decorators import customer_required
from utilities.enums import Status



app = Flask(__name__)


app.config.from_object("config")

jwt = JWTManager(app)

database.init_app(app)


@app.context_processor
def user_name():
    identity = get_jwt_identity()
    return {"mail":identity}


@app.route("/", methods=["GET"])
@customer_required()
def profile():
    user = get_user_info()
    return render_template("home_customer.html",user=user)



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
        return render_template("search_results.html", categories=categories, products=products)

    return render_template("search.html")

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
                #Update waiting column
                update_product_waiting(product_exist,product_quant)
            
            if sending_req == []:
                raise ErrorHandler("Please pick a product to order.",400)

        except ErrorHandler as e:
            flash(e.message,"danger")
            return render_template("order.html", products=products)
        
        order = add_order(get_email(),Status.CREATED.name)
        database.session.commit()

        for x in sending_req:
            add_order_product(order.id,int(x['id']), int(x['quantity']))

        database.session.commit()

        flash(f"Order with id:{order.id} is successfully created!","success")

    return render_template("order.html", products=products)

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

            if order_exists.status == Status.CREATED.name:
                raise ErrorHandler("Order is not picked up by courier be patient.",400)


        except ErrorHandler as e:
            flash(e.message,"danger")
            return render_template("delivered.html",orders=orders)
    
        change_status_of_order(order_exists,Status.COMPLETED.name)

        for order_product in order_exists.products:
            update_product_sold(order_product.product,order_product.quantity)
        
        flash(f"Order with id:{order_id} is successfully delivered!","success")


    return render_template("delivered.html",orders=orders)


@app.route("/logout",methods=["POST"])
def logout():
    return logout_user()

@jwt.expired_token_loader
def handle_expired_token(jwt_header,jwt_payload):
    return expired_token()

@jwt.invalid_token_loader
def handle_invalid_token(reason):
    return invalid_token()


@jwt.unauthorized_loader
def unauthorized_error(reason):
    return unauthorized_access()


if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0")