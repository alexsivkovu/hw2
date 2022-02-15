dbhandle = pw.PostgansqlDatabase(
    db_name, user=user_name,
    password=password,
    host='localhost'
)

app = flask.Flask(__name__)


class BaseModel(pw.Model):
    class Meta:
        database = dbhandle


class initial_model(BaseModel):
    id = pw.PrimaryKeyField(null=False)
    number = pw.IntegerField(unique=True)


if __name__ == '__main__':
    try:
        dbhandle.connect()
        initial_model.create_table()
    except pw.InternalError as px:
        print(str(px))



@app.route("/number", methods=['POST'])
def addnumber():
    data = flask.request.data
    num = json.loads(data)['number']
    ans = initial_model.select().where(
        (initial_model.number == num) |
        (initial_model.number == (num - 1))
    )
    if len(ans) == 0:
        ans = initial_model.create(number=num)
        return {'number': num + 1}
    else:
        if len(ans) == 2:
            return {'code': 500,
                    'message': 'Both entries of the number and the number less by one are already in the database'}, 500
        elif ans[0].number == num:
            return {'code': 500, 'message': 'This number are already in the database'}, 500
        else:
            return {'code': 500, 'message': 'Number less by one are already in the database'}, 500