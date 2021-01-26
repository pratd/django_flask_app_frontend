from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
from sqlalchemy import UniqueConstraint 


app = Flask(__name__)
sql_user=os.environ.get('SQL_USER')
sql_password=os.environ.get('SQL_PASSWORD')
sql_db=os.environ.get('DATABASE_NAME')
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://'+sql_user+':'+sql_password+'@db/'+sql_db
CORS(app)

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False) # doesnot create but gets form django app
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))


class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')

@app.route('/')
def index():
    return 'Hello'

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0') 