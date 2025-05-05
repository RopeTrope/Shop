FROM python:3.12.2

WORKDIR /usr/local/app

COPY authentication .
RUN pip install -r ./requirements.txt



ENTRYPOINT [ "python","./authentication.py" ]