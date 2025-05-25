FROM python:3.12.2

WORKDIR /usr/local/app

COPY ./shop/requirements.txt .

RUN pip install -r ./requirements.txt

COPY ./shop/owner.py .
COPY ./shop/keys.json .
COPY ./shop/models ./models
COPY  ./shop/templates/base_owner.html ./templates/base_owner.html
COPY ./shop/templates/update.html ./templates/update.html
COPY ./shop/templates/home_owner.html ./templates/home_owner.html
COPY ./shop/config.py .
COPY ./shop/utilities ./utilities



ENTRYPOINT [ "python","./owner.py" ]