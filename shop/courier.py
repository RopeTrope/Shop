from flask import Flask, render_template, request, jsonify
from models.models import database


from utilities.databaseUtils import get_all_not_taken_orders, get_order_only_by_id, change_status_of_order
from utilities.enums import Status
from utilities.exceptions import ErrorHandler


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

database.init_app(app)


#TODO: Add access control
#TODO: Should change in other routes to show id of order and not indexing
@app.route("/orders_to_deliver",methods=["GET"])
def orders_to_deliver():
    orders = get_all_not_taken_orders()
    return render_template("orders_to_deliver.html",orders=orders)

@app.route("/pick_up_order",methods=["GET","POST"])
def pick_up_order():

    if request.method == "POST":
        order_id = request.form.get("orderId")
        try:
            if order_id is None:
                raise ErrorHandler("Missing order id.",400)
            
            order_exists = get_order_only_by_id(order_id)
            if order_exists is None:
                raise ErrorHandler("Invalid order id.",400)
        except ErrorHandler as e:
            return jsonify({"message":e.message}),e.error_code
        
        change_status_of_order(order_exists,Status.PENDING.name)

    orders = get_all_not_taken_orders()
        
    return render_template("pick_up_order.html",orders=orders)
    


if __name__=="__main__":
    app.run(debug=True,port=5300)