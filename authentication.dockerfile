FROM python:3.12.2

WORKDIR /usr/local/app

COPY requirements.txt ./
RUN pip install -r ./requirements.txt

COPY templates ./templates
COPY authentication.py ./
COPY databaseUtils.py ./
COPY keys.json ./
COPY models.py ./
COPY utilities.py ./
COPY startup.sh ./

ENV FLASK_APP=authentication.py

RUN chmod +x ./startup.sh



ENTRYPOINT [ "./startup.sh" ]