FROM python:3.12.2

WORKDIR /usr/local/app

COPY authentication/requirements.txt .

RUN pip install -r ./requirements.txt

COPY authentication .




ENTRYPOINT [ "python","./authentication.py" ]