import logging, json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal   # setelah install flask_restful
import datetime
from datetime import timedelta
from flask_jwt_extended import jwt_required, get_jwt_claims

from . import *
from blueprints.user import *
from blueprints.items import *

bp_cart = Blueprint('cart', __name__)
api = Api(bp_cart)

class CartResource(Resource) :

    def __init__(self) :
        pass

    @jwt_required
    def get(self, transaction_id = None) :
        if id is None :
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default =  1)
            parser.add_argument('rp', type = int, location = 'args', default =  5)
            parser.add_argument('transaction_id', type = int, location = 'args')
            parser.add_argument('item_id', type = int, location = 'args')

            args = parser.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']

            qry = Cart.query
            
            if args['transaction_id'] is not None :
                qry = qry.filter_by(book_id=args['transaction_id'])
            if args['item_id'] is not None :
                qry = qry.filter_by(user_id=args['item_id'])

            rows = []
            for row in qry.limit(args['rp']).offset(offset).all() :
                carts = marshal(row, Cart.response_field)
                users = User.query.get(row.user_id)
                carts['users'] = marshal(users, User.response_field)
                items = Item.query.get(row.item_id)
                carts['items'] = marshal(items, Items.response_field)
                rows.append(carts)
            return rows, 200, {'Content-Type' : 'application/json'}

        else :
            qry = Cart.query.get(id)       
            qry = marshal(qry, Cart.response_field)
            row = []
            # for row in qry.limit(args['rp']).offset(offset).all() :
            # users = User.query.get(row.user_id)
            carts = Cart.query.get(qry['user_id'])
            qry['users'] = marshal(users, Users.response_field)
            items = Item.query.get(qry['item_id'])
            qry['items'] = marshal(items, Item.response_field)
            if qry is not None :
                return qry, 200, {'Content-Type' : 'application/json'}
            return {'status' : 'NOT_FOUND', 'message' : 'Data not Found'}, 404, {'Content-Type' : 'application/json'}

    # @jwt_required
    def post(self) :
        jwtClaims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='json', type = int, required = True)
        parser.add_argument('item_id', location='json', type = int, required = True)
        parser.add_argument('total_harga', location='json', type = int, required = True)
        args = parser.parse_args()
        # returndate = datetime.datetime.today() + timedelta(days=7)
        # return_date = str(returndate)
        # args['post_by'] = jwtClaims['user_id']

        cart = Cart(None, args['user_id'], args['item_id'], args['total_harga'])
        db.session.add(cart)
        db.session.commit()

        cart = marshal(cart, Cart.response_field)
        users = User.query.get(args['user_id'])
        cart['user'] = marshal(users, User.response_field)
        items = Item.query.get(args['item_id'])
        cart['item'] = marshal(items, Item.response_field)

        return cart, 200, {'Content-Type' : 'application/json'}

    

api.add_resource(CartResource, '/user/cart', '/user/cart/<int:id>')