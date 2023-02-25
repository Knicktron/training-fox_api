from flask import Flask, jsonify
from flask_sqlalchemy import MySQL
import json


class GetDBConfig:
    def __init__(self, path_to_file=None):
        with open(path_to_file) as db_config_file:
            db_config = json.load(db_config_file)

        self.hostname = db_config["hostname"]
        self.port = db_config["port"]
        self.username = db_config["username"]
        self.password = db_config["password"]
        self.dbname = db_config["database"]

dbconf = GetDBConfig("data/dbconf.json")

app = Flask(__name__)
app.config["MYSQL_HOST"] = dbconf.hostname
app.config["MYSQL_PORT"] = dbconf.port
app.config["MYSQL_USER"] = dbconf.username
app.config["MYSQL_PASSWORD"] = dbconf.password
app.config["MYSQL_DB"] = dbconf.dbname
db = MySQL(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(80), nullable=False)
    firstname = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"{self.firstname} {self.surname}"





@app.route('/')
def index():
    return 'Hello'

@app.route('/users')
def get_users():
    cursor = db.connection.cursor()
    cursor.execute('''SELECT id, firstname, surname FROM train.users''')
    raws = cursor.fetchall()
    users = []
    for raw in raws:
        user = {
            'id': raw[0],
            'firstname': raw[1],
            'surname': raw[2]
        }
        users.append(user)
    return jsonify(users)
