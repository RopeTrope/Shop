from flask import Flask, render_template, request, flash
from flask_jwt_extended import JWTManager, get_jwt_identity
from models.models import database


from utilities.utilities import get_user_info, unauthorized_access, expired_token, invalid_token, logout_user
from utilities.decorators import courier_required
from utilities.databaseUtils import get_all_not_taken_orders, get_order_only_by_id, change_status_of_order
from utilities.enums import Status
from utilities.exceptions import ErrorHandler



app = Flask(__name__)

app.config.from_object("config")

jwt = JWTManager(app)

database.init_app(app)

@app.context_processor
def user_name():
    identity = get_jwt_identity()
    return {"mail":identity}


@app.route("/", methods=["GET"])
@courier_required()
def profile():
    user = get_user_info()
    return render_template("home_courier.html",user=user)






@app.route("/orders_to_deliver",methods=["GET"])
@courier_required()
def orders_to_deliver():
    orders = get_all_not_taken_orders()
    return render_template("orders_to_deliver.html",orders=orders)

@app.route("/pick_up_order",methods=["GET","POST"])
@courier_required()
def pick_up_order():
    orders = get_all_not_taken_orders()
    if request.method == "POST":
        order_id = request.form.get("orderId")
        try:
            if order_id is None:
                raise ErrorHandler("Missing order id.",400)
            
            order_exists = get_order_only_by_id(order_id)
            if order_exists is None:
                raise ErrorHandler("Invalid order id.",400)
            
            if order_exists.status != Status.CREATED.name:
                raise ErrorHandler("Order is already picked up.",400)
            
        except ErrorHandler as e:
            flash(e.message,"danger")
            return render_template("pick_up_order.html",orders=orders)
        
        change_status_of_order(order_exists,Status.PENDING.name)
        flash(f"Order with id:{order_id} is picked successfully! Please refresh the page.","success")
        
    return render_template("pick_up_order.html",orders=orders)

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