from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

MYSQL_ROOT_PASSWORD = os.environ.get("MYSQL_ROOT_PASSWORD")
MYSQL_HOST = os.environ.get("MYSQL_HOST")
sqlurl = 'mysql+pymysql://root:' + MYSQL_ROOT_PASSWORD + '@' + MYSQL_HOST + ':3306/test'
    
Base = declarative_base()
engine = create_engine(sqlurl)

app.config['SQLALCHEMY_DATABASE_URI'] = sqlurl
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Base.metadata.reflect(engine)

class Test(Base):
    __tablename__ = 'tourist_attraction'
    __table_args__ = {'extend_existing': True,
                      'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True)
    a = db.Column(db.Text)
    
    def __init__(self, a):
        self.a = a
        
    def serialize(self):
        return {
            'a' : self.a
        }
        
Base.metadata.create_all(engine)
