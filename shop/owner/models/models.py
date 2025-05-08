from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


product_category = database.Table(
    'product_category',
    database.Column('product_id',database.Integer, database.ForeignKey('products.id'), primary_key=True),
    database.Column('category_id',database.Integer, database.ForeignKey('categories.id'), primary_key=True)
)


#TODO: Need to add third table for this
class Product(database.Model):
    __tablename__='products' 
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    name = database.Column(database.String(64), nullable=False)
    price = database.Column(database.Double, nullable=False)
    categories = database.relationship('Category', secondary=product_category, backref='products')


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
