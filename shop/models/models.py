from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


product_category = database.Table(
    'product_category',
    database.Column('product_id',database.Integer, database.ForeignKey('products.id'), primary_key=True),
    database.Column('category_id',database.Integer, database.ForeignKey('categories.id'), primary_key=True)
)



class Product(database.Model):
    __tablename__='products' 
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    name = database.Column(database.String(64), nullable=False)
    price = database.Column(database.Double, nullable=False)
    categories = database.relationship('Category', secondary=product_category, backref='products')

    orders = database.relationship('OrderProduct',back_populates='product')


    def __init__(self,name,price):
        self.name = name
        self.price = price
        self.categories = []

class Category(database.Model):
    __tablename__='categories'
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    name = database.Column(database.String(64), nullable=False)

    def __init__(self,name):
        self.name = name

class Order(database.Model):
    __tablename__ = "orders"
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    email = database.Column(database.String(256),nullable=False)
    status = database.Column(database.String(32),nullable=False)
    timestamp = database.Column(database.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    #Probably will add email of a user
    products = database.relationship("OrderProduct", back_populates='order')

    def __init__(self,email,status):
        self.email = email
        self.status = status

class OrderProduct(database.Model):
    __tablename__='order_product'
    order_id = database.Column(database.Integer,database.ForeignKey('orders.id'),primary_key=True)
    product_id = database.Column(database.Integer,database.ForeignKey('products.id'),primary_key=True)

    quantity = database.Column(database.Integer, nullable=False)

    order = database.relationship('Order', back_populates='products')
    product = database.relationship('Product', back_populates='orders')

    def __init__(self,order_id,product_id,quantity):
        self.product_id = product_id
        self.order_id = order_id
        self.quantity = quantity





