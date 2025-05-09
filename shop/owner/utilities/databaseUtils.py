from models.models import Product, Category
from models.models import database
from .exceptions import ErrorHandler

def check_product_exist(name):
    product_exists = Product.query.filter_by(name=name).first()
    if product_exists:
        database.session.rollback()
        raise ErrorHandler(f"Product {name} already exists.",400)
    return product_exists

def add_product(name,price):
    product = Product(name,float(price))
    database.session.add(product)
    return product

def add_category_to_product(category,product):
    category_exists = check_category_exist(category)
    if not category_exists:
        category = Category(category)
        product.categories.append(category)
    else:
        product.categories.append(category_exists)


def check_category_exist(name):
    return Category.query.filter_by(name=name).first()
