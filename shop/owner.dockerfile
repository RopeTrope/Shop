FROM python:3.12.2

WORKDIR /usr/local/app

COPY ./shop/requirements.txt .
COPY ./shop/owner.py .
COPY ./shop/keys.json .
COPY ./shop/models ./models
COPY ./shop/templates/update.html ./templates/update.html
COPY ./shop/config.py .
COPY ./shop/utilities ./utilities

RUN pip install -r ./requirements.txt

ENTRYPOINT [ "python","./owner.py" ]