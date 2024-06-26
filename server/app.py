#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    all_bakeries = Bakery.query.all()
    bakery_list = []
    for bakery in all_bakeries:
        bakery_data = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        bakery_list.append(bakery_data)
    return jsonify(bakery_list)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    bakery_data = {
        'id': bakery.id,
        'name': bakery.name,
        'created_at': bakery.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(bakery_data)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = []
    for baked_good in baked_goods:
        baked_good_data = {
            'id': baked_good.id,
            'name': baked_good.name,
            'price': baked_good.price,
            'created_at': baked_good.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        baked_goods_list.append(baked_good_data)
    return jsonify(baked_goods_list)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive:
        baked_good_data = {
            'id': most_expensive.id,
            'name': most_expensive.name,
            'price': most_expensive.price,
            'created_at': most_expensive.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify(baked_good_data)
    else:
        return jsonify({'message': 'No baked goods found.'}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
