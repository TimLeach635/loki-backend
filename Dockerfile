FROM python:3.6

RUN pip install flask flask-sqlalchemy flask-cors psycopg2-binary

ENV FLASK_APP loki.py

COPY loki.py loki.py
COPY config.py config.py
COPY app app

ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
