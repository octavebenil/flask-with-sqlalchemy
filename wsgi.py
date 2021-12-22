'''
import os
import logging
logging.warn(os.environ["DUMMY"])
'''
from flask import Flask, request, abort
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy(app)
ma = Marshmallow(app)

from flask_migrate import Migrate

from models import Product

migrate = Migrate(app, db)

BASE_URL = "/api/v1"

from schemas import many_product_schema, one_product_schema

@app.route(f'{BASE_URL}/products', methods=['GET'])
def get_many_product():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return many_product_schema.jsonify(products), 200


@app.route(f"{BASE_URL}/products/<int:id>", methods=["GET"])
def read_one_product(id):
    product = db.session.query(Product).get(id)
    if not product:
        abort(404)
    else:
        return one_product_schema.jsonify(product), 200


@app.route(f"{BASE_URL}/products", methods=["POST"])
def create_one_product():
    post = request.get_json()

    if not post["name"]:
        abort(422)
    else:
        new_product = Product()
        new_product.name = post["name"]

        db.session.add(new_product)
        db.session.commit()

        return one_product_schema.jsonify(new_product), 201

@app.route(f"{BASE_URL}/products/<int:id>", methods=["PATCH"])
def update_one_product(id):
    post = request.get_json()

    if not post["name"]:
        abort(422)
    else:
        product = db.session.query(Product).get(id)

        if not product:
            abort(404)
        else:
            product.name = post["name"]
            db.session.commit()
            return one_product_schema.jsonify(product), 200


@app.route(f"{BASE_URL}/products/<int:id>", methods=["DELETE"])
def delete_one_product(id):
    post = request.get_json()

    product = db.session.query(Product).get(id)
 
    if not product:
        abort(404)
    else:
        db.session.delete(product)
        db.session.commit()

    return "", 204