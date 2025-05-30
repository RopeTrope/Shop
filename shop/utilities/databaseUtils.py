from models.models import Product, Category, Order, OrderProduct, product_category
from models.models import database
from .enums import Status




def add_product(name,price):
    product = Product(name,float(price))
    database.session.add(product)
    return product

def add_order(email,status):
    order = Order(email,status)

    database.session.add(order)
    return order

def add_order_product(order_id,product_id,quantity):
    order_product = OrderProduct(order_id,product_id,quantity)
    database.session.add(order_product)



def add_category_to_product(category,product):
    category_exists = check_category_exist(category)
    if not category_exists:
        category = Category(category)
        product.categories.append(category)
    else:
        product.categories.append(category_exists)


def change_status_of_order(order,status):
    order.status = status
    database.session.commit()

def check_category_exist(name):
    return Category.query.filter_by(name=name).first()


def check_product_on_id(product_id):
    return Product.query.filter(Product.id == product_id).first()

def check_product_exist(name):
    product_exists = Product.query.filter_by(name=name).first()
    return product_exists

def get_all_products():
    return Product.query.all()

def get_my_orders(email):
    return Order.query.join(OrderProduct).join(Product).filter(Order.email ==email).all()

def get_my_order_by_id(id,email):
    return Order.query.filter(Order.id == id, Order.email == email).one()

def get_order_only_by_id(id):
    return Order.query.filter(Order.id == id).one()

def get_all_not_taken_orders():
    return Order.query.filter(Order.status == Status.CREATED.name).all()

def get_products_by_order_id(order_id):
    return Product.query.join(OrderProduct).filter(OrderProduct.order_id == order_id).all()

def get_categories_by_product_id(product_id):
    return Category.query.join(product_category).filter(product_category.c.product_id == product_id).all()

def get_quantity(order_id,product_id):
    return OrderProduct.query.filter(OrderProduct.order_id == order_id, OrderProduct.product_id == product_id).one()

def get_all_products_from_order(email):
    return Product.query.join(OrderProduct).join(Product).filter(Order.email == email).all()

def search_categories_on_name(search_category, search_product):
    return Category.query.join(product_category).join(Product).filter(Category.name.like(search_category),Product.name.like(search_product)).all()

def search_products_on_name(search_category, search_product):
    return Product.query.join(product_category).join(Category).filter(Category.name.like(search_category),Product.name.like(search_product)).all()

def update_product_waiting(product:Product,quantity):
    product.waiting += int(quantity)

def update_product_sold(product:Product,quantity):
    product.sold += int(quantity)
    product.waiting -= int(quantity)
    database.session.commit()