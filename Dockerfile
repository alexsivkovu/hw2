FROM python:3.9

RUN apt-get update &&\
apt upgrade -y
RUN apt install postgresql postgresql-contrib -y
RUN apt-get install python3-pip -y
RUN pip3 install Flask
RUN pip3 install SQLAlchemy
RUN pip3 install -U Flask-SQLAlchemy
RUN pip3 install Flask-Migrate
RUN pip3 install psycopg2-binary
COPY venv/app.py /app.py
COPY venv/config.py /config.py
COPY entrypoint.sh /entrypoint.sh

RUN python --version
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["run"]
RUN cat /app.py
