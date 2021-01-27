from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
from sqlalchemy import UniqueConstraint 
from dataclasses import dataclass
import requests
from producer import publish

app = Flask(__name__)
sql_user=os.environ.get('SQL_USER')
sql_password=os.environ.get('SQL_PASSWORD')
sql_db=os.environ.get('DATABASE_NAME')
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://'+sql_user+':'+sql_password+'@db/'+sql_db
CORS(app)

db = SQLAlchemy(app)

@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str
    id = db.Column(db.Integer, primary_key=True, autoincrement=False) # doesnot create but gets form django app
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

@dataclass
class ProductUser(db.Model):
    id: int
    user_id: int
    product_id: int
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')

@app.route('/api/products')
def index():
    return jsonify(Product.query.all())

@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get('http://docker.for.win.localhost:8000/api/user')
    json = req.json()
    print(json)
    try:
        productUser = ProductUser(user_id=json['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()
        #event

        publish('product liked', id)
    except:
        abort(400, 'You already liked this product')

    return jsonify({
        'message' :'success'
    })


if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0') 