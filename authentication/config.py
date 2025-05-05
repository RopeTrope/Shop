import json
from datetime import timedelta

DATABASE_USERNAME="user"
DATABASE_PASSWORD="user"
DATABASE_NAME="db"
DATABASE_PORT=3306
DATABASE="Shop"

with open('keys.json','r') as file:
    data = json.load(file)
    secret_key = data["SECRET_TOKEN"]


SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_NAME}:{DATABASE_PORT}/{DATABASE}'
JWT_SECRET_KEY=secret_key
JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1)
JWT_TOKEN_LOCATION=["cookies"]
JWT_COOKIE_CSRF_PROTECT=False
