import json
from datetime import timedelta
import os

DATABASE_USERNAME="user"
DATABASE_PASSWORD="user"
DATABASE_NAME="db_shop"
DATABASE_PORT=3306
DATABASE="Shop"

SPARK_NAME="sparkapp"
SPARK_PORT=5400
SPARK_PRODUCT_STATISTICS_ROUTE="product_statistics"
SPARK_CATEGORY_STATISTICS_ROUTE="category_statistics"

cwd = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(cwd,'keys.json')

with open(file_path,'r') as file:
    data = json.load(file)
    secret_key = data["SECRET_TOKEN"]

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_NAME}:{DATABASE_PORT}/{DATABASE}'
JWT_SECRET_KEY=secret_key
JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1)
JWT_TOKEN_LOCATION=["cookies"]
JWT_COOKIE_CSRF_PROTECT=False

