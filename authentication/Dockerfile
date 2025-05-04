FROM python:3.12.2

WORKDIR /usr/local/app

COPY requirements.txt ./
RUN pip install -r ./requirements.txt

COPY authentication ./authentication

RUN chmod +x ./authentication/scripts/startup.sh

ENTRYPOINT [ "./authentication/scripts/startup.sh" ]