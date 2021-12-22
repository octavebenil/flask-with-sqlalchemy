'''
import os
import logging
logging.warn(os.environ["DUMMY"])
'''
from flask import Flask
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

from schemas import many_product_schema

@app.route(f'{BASE_URL}/products', methods=['GET'])
def get_many_product():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return many_product_schema.jsonify(products), 200