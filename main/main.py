from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS


app = Flask(__name__)
sql_user=os.environ.get('MYSQL_USER')
sql_password=os.environ.get('MYSQL_PASSWORD')
sql_db=os.environ.get('MYSQL_DATABASE')
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql:/$(sql_user):$(sql_password)@db/$(sql_db)'
CORS(app)

db = SQLAlchemy(app)

class Product(db.Model):
    id=db.Column(db.Integer, primary_key=True, autoincrement=False) # doesnot create but gets form django app


@app.route('/')
def index():
    return 'Hello'

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0') 