FROM python:3.12.2

WORKDIR /usr/local/app

COPY ./shop/requirements.txt .
COPY ./shop/courier.py .
COPY ./shop/keys.json .
COPY ./shop/models ./models
COPY ./shop/templates/pick_up_order.html ./templates/pick_up_order.html
COPY ./shop/templates/orders_to_deliver.html ./templates/orders_to_deliver.html
COPY ./shop/config.py .
COPY ./shop/utilities ./utilities

RUN pip install -r ./requirements.txt

ENTRYPOINT [ "python","./courier.py" ]