import logging, json
from flask_restful import Resource, Api, reqparse, abort, marshal
from flask import Blueprint, Flask, request
from blueprints import db
from blueprints.book import Book
from blueprints.user import User
from flask_jwt_extended import jwt_required, get_jwt_claims

from . import *

bp_transactions = Blueprint('transactions', __name__)
api = Api(bp_transactions)

class TransactionResouce(Resource):
    @jwt_required
    def get(self, id=None):
        if id is None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=5)
            parser.add_argument('cart_id', type=int, location='args')
            parser.add_argument('user_id', type=int, location='args')
            args = parser.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']  
            
            qry = TransactionResouce.query

            if args['cart_id'] is not None:
                qry = qry.filter_by(name=args['cart_id'])

            if args['user_id'] is not None:
                qry = qry.filter_by(name=args['user_id'])

            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                
                temp = marshal(row, Transaction.response_field)
                qry_1 = Cart.query.get(temp['transaction_id'])
                qry_2 = Item.query.get(temp['item_id'])

                temp['transaction'] = marshal(qry_1, Cart.response_field)
                temp['item'] = marshal(qry_2, User.response_field)
                rows.append(temp)

            return rows, 200, {'Content-Type': 'application/json'}

        else:
            qry = Transaction.query.get(id) # SELECT * FROM Book WHERE id = id
            if qry is not None:
                temp = marshal(qry, Rent.response_field)
                qry_1 = Cart.query.get(temp['transaction_id'])
                qry_2 = Item.query.get(temp['item_id'])

                temp['book'] = marshal(qry_1, Book.response_field)
                temp['user'] = marshal(qry_2, User.response_field)

                return temp, 200, {'Content-Type': 'application/json'}

            return {'status': 'NOT_FOUND', 'message': 'Transaction not found'}, 404, {'Content-Type': 'application/json'}


    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        
        parser.add_argument('transaction_id', type=int, location='json', required=True)
        parser.add_argument('item_id', type=int, location='json', required=True)

        args = parser.parse_args()

        qry_1 = Cart.query.get(args['transaction_id'])
        qry_2 = User.query.get(args['user_id'])

        if qry_1 is None or qry_2 is None:
            return {"Message": "transaction id or user id not found"}, 404, {'Content-Type': 'application/json'}

        return_date = "2019-02-23"
        post_by = get_jwt_claims()['status']
        transaction = Transaction(None, args['transaction_id'], args['user_id'], return_date, post_by)

        db.session.add(transaction)
        db.session.commit()

        temp = marshal(transaction, Transaction.response_field)
        temp['user'] = marshal(qry_2, User.response_field)
        temp['cart'] = marshal(qry_1, Cart.response_field)

        return temp, 200, {'Content-Type': 'application/json'}

api.add_resource(TransactionResource, '/user/transaction', '/user/transaction/<int:cart_id>')