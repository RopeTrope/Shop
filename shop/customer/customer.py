from flask import Flask, render_template, request, jsonify

from models.models import Product, Category, product_category, database


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

database.init_app(app)


@app.route("/search",methods=["GET","POST"])
def search():
    if request.method == "POST":
        product_name = request.form.get("pname")
        search_product = "%{}%".format(product_name)
        category_name = request.form.get("category")
        search_category = "%{}%".format(category_name)

        categories = Category.query.join(product_category).join(Product).filter(Category.name.like(search_category),Product.name.like(search_product)).all()
        products = Product.query.join(product_category).join(Category).filter(Category.name.like(search_category),Product.name.like(search_product)).all()
        json_products = []
        for product in products:
            json_products.append({"categories":[category.name for category in product.categories],"id":product.id,"name":product.name,"price":product.price})

        return jsonify({"categories":[category.name for category in categories],"products":[product for product in json_products]}),200

    return render_template("search.html")

if __name__=="__main__":
    app.run(debug=True,port=5200)