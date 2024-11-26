#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(  bakeries,   200  )

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    bakery_serialized = bakery.to_dict()
    return make_response ( bakery_serialized, 200 )

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized, 200)

@app.route('/baked_goods', methods = ['GET','POST'])
def creat_baked_goods():
        data = request.form
        baked_good = BakedGood(name=data.get("name"), price=data.get('price'),bakery_id=data.get('bakery_id'))
        db.session.add(baked_good)
        db.session.commit()
        response = make_response(baked_good.to_dict(),201)

   
        return response

#PATCH bakery name
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery_name(id):
    bakery =Bakery.query.get_or_404(id)
    bakery.name= request.form.get('name', bakery.name)
    db.session.commit()
    response = make_response(bakery.to_dict(),200)
    return response

@app.route('/baked_goods/<int:id>', methods= ['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get_or_404(id)
    db.session.delete(baked_good)
    db.session.commit()
    response = make_response({'message':'Baked god deleted sucessflly'},200)




if __name__ == '__main__':
    app.run(port=5555, debug=True)