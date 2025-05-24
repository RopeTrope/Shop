import json
from flask import Flask,render_template, redirect
import os
import subprocess
app = Flask(__name__)

@app.route("/product_statistics")
def product_statistics():
    os.environ["SPARK_APPLICATION_PYTHON_LOCATION"] = "/app/product_statistics.py"
    os.environ["SPARK_SUBMIT_ARGS"] = "--driver-class-path /app/mysql-connector-j-9.3.0.jar --jars /app/mysql-connector-j-9.3.0.jar"
    
    result = subprocess.check_output(["/template.sh"]).decode()

    #Delete this file after read
    with open("/app/result.json","r") as f:
        data = json.load(f)


    return render_template("product_statistics.html", products=data["statistics"])

@app.route("/update")
def update():
    return redirect("http://localhost:5100/update")


@app.route("/category_statistics")
def category_statistics():
    os.environ["SPARK_APPLICATION_PYTHON_LOCATION"] = "/app/category_statistics.py"
    os.environ["SPARK_SUBMIT_ARGS"] = "--driver-class-path /app/mysql-connector-j-9.3.0.jar --jars /app/mysql-connector-j-9.3.0.jar"

    result = subprocess.check_output(["/template.sh"]).decode()

    with open("/app/result2.json","r") as f:
        data = json.load(f)

    return render_template("category_statistics.html",categories=data["statistics"])

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=5400)