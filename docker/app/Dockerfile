FROM python:3.6.5

EXPOSE 8080

ADD . /deploy

WORKDIR /deploy

RUN pip install -r requirements.txt

CMD python wsgi.py
