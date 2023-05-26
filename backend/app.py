from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask import Flask, request
from dotenv import load_dotenv
from flask_restx import Resource, Api
from sqlalchemy_utils import database_exists, create_database
from models import db
import os, models

app = Flask(__name__)
load_dotenv()
api = Api(app)

MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_ROOT_PASSWORD = os.environ.get("MYSQL_ROOT_PASSWORD")
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")
MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_PORT = os.environ.get("MYSQL_PORT")

sqlurl = 'mysql+pymysql://root:' + MYSQL_ROOT_PASSWORD + '@' + MYSQL_HOST + ':3306/test'
engine = create_engine(sqlurl)

app.config['MYSQL_DB'] = MYSQL_USER
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['SQLALCHEMY_DATABASE_URI'] = sqlurl
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ns = api.namespace('/', description='Server Lecture API')

with app.app_context():
    if not database_exists(sqlurl):
        create_database(sqlurl)

request_schema = {
    'a': 'str'
}

a_request_model = api.schema_model('a_request_model', request_schema)


@ns.route("/api/<int:first>/<int:second>", methods=['GET'])
class SumApi(Resource):
    def get(self, first, second):
        return ({'result' : first+second}, 200)

@ns.route("/api/test", methods=['POST', 'GET'])
class BodyApi(Resource):
    @api.expect(a_request_model, validate=True)
    def post(self):
        req_data = request.get_json()
        row = models.Test(a=req_data['a'])
        db.session.add(row)
        db.session.commit()
        return ("success", 200)
    
    def get(self):
        res : list(models.Test) = db.session.query(models.Test).all()
        return (list(map(lambda o: o.serialize(), res)), 200)

@ns.route("/api/test/<int:id>", methods=['GET', 'PUT', 'DELETE'])
class FindOne(Resource):
    def get(self, id):
        ret = db.session.query(models.Test).filter(models.Test.id == id).first()
        return (ret.serialize(), 200)
    
    @api.expect(a_request_model, validate=True)
    def put(self, id):
        row = db.session.query(models.Test).filter(models.Test.id == id).first()
        row.a = request.get_json()['a']
        db.session.commit()
        return ("success", 200)
    
    def delete(self, id):
        row = db.session.query(models.Test).filter(models.Test.id == id).first()
        db.session.delete(row)
        db.session.commit()
        return ("success", 200)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
