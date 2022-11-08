FROM python:3.9
LABEL author="Humai <admin@humai.com.ar>"

# RUN apt-get update && apt-get upgrade

COPY ./ .
COPY ./src .
ENV GOOGLE_APPLICATION_CREDENTIALS ./alumnos-sandbox-50f796a33b0b.json


RUN pip3 install -r requirements.txt

CMD python3 main.py
