FROM python:3.12.2

WORKDIR /usr/local/app

COPY ./shop/requirements.txt .
COPY ./shop/customer.py .
COPY ./shop/keys.json .
COPY ./shop/models ./models
COPY ./shop/templates/base_customer.html ./templates/base_customer.html
COPY ./shop/templates/search.html ./templates/search.html
COPY ./shop/templates/search_results.html ./templates/search_results.html
COPY ./shop/templates/order.html ./templates/order.html
COPY ./shop/templates/status.html ./templates/status.html
COPY ./shop/templates/delivered.html ./templates/delivered.html
COPY ./shop/config.py .
COPY ./shop/utilities ./utilities

RUN pip install -r ./requirements.txt

ENTRYPOINT [ "python","./customer.py" ]