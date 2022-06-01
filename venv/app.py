from config import default_db_conf
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from typing import Union
import os

app = Flask(__name__)

# make config
db_config = {}
for var in ['DB_USER_NAME', 'DB_USER_PASSWORD', 'DB_NAME', 'DB_HOST']:
    try:
        db_config.update({
            var: os.environ[var]
        })
    except KeyError:
        print('%s variable does not exist in environment' % var)
        db_config.update({
            var: default_db_conf['DEFAULT_' + var]
        })

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://%(user_name)s:%(password)s@%(host)s/%(db)s' % ({
        'user_name': db_config['DB_USER_NAME'],
        'password': db_config['DB_USER_PASSWORD'],
        'host': db_config['DB_HOST'],
        'db': db_config['DB_NAME']
    })

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'ea2c4ed0-721e-4e3b-985f-3397a2a67837'
db = SQLAlchemy(app)


class Number(db.Model):
    __tablename__ = 'Number'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer())


def __init__(self, value):
    self.value = value


db.create_all()
migrate = Migrate(app, db)


@app.route('api/v1/')
def start_page() -> None:
    """
    The initial check of app
    :return: if works, returns 200 response
    """
    return {
        'code': 200,
        'message': 'The application is up'
    }


@app.route('api/v1/truncate')
def truncate() -> dict[str, Union[int, str]]:
    """
    Truncate nubers table
    :return: if works, returns 200 response
    """
    try:
        db.session.query(Number).delete()
        db.session.commit()
    except:
        db.session.rollback()

    return {
        'code': 200,
        'message': 'The Number table has been truncated'
    }


@app.route('api/v1/numbers', methods=['POST'])
def nums():
    if request.method == 'POST':
        if request.is_json:
            new_num_value = request.get_json()['number']
            check = [i.value for i in db.session.query(Number).filter(
                Number.value.in_([new_num_value, new_num_value - 1])).all()]
            if not check:
                new_num = Number(value=request.get_json()['number'])
                db.session.add(new_num)
                db.session.commit()
                return {
                    'code': 200,
                    'value': new_num_value,
                    "message": f"number {new_num_value} has been created successfully."}
            else:
                if len(check) == 2:
                    return {
                        'code': 501,
                        "message": f"number {new_num_value} already exists and also number-1 exists."}
                elif (len(check) == 1) & (check[0] == new_num_value):
                    return {
                        'code': 501,
                        "message": f"number {new_num_value} already exists."}
                elif (len(check) == 1) & (check[0] == new_num_value - 1):
                    return {
                        'code': 501,
                        "message": f"number {new_num_value} is bigger than one nuber that already exists."}
        else:
            return {'code': '400',
                    'error': 'The request data is not in JSON format'}
    else:
        return {'code': '400',
                'error': 'The request method is not POST'}


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
