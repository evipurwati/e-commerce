import logging, json
from flask_restful import Resource, Api, reqparse, abort, marshal
from flask import Blueprint, Flask, request
from blueprints import db
from blueprints.book import Book
from blueprints.user import User
from flask_jwt_extended import jwt_required, get_jwt_claims

from . import *

bp_rent = Blueprint('rent', __name__)
api = Api(bp_rent)

class RentResource(Resource):

    def get(self, id=None):
        if id is None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=5)
            parser.add_argument('book_id', type=int, location='args')
            parser.add_argument('user_id', type=int, location='args')
            args = parser.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']  
            
            qry = Rent.query

            if args['book_id'] is not None:
                qry = qry.filter_by(name=args['book_id'])

            if args['user_id'] is not None:
                qry = qry.filter_by(name=args['user_id'])

            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                
                temp = marshal(row, Rent.response_field)
                qry_1 = Book.query.get(temp['book_id'])
                qry_2 = User.query.get(temp['user_id'])

                temp['book'] = marshal(qry_1, Book.response_field)
                temp['user'] = marshal(qry_2, User.response_field)
                rows.append(temp)

            return rows, 200, {'Content-Type': 'application/json'}

        else:
            qry = Rent.query.get(id) # SELECT * FROM Book WHERE id = id
            if qry is not None:
                temp = marshal(qry, Rent.response_field)
                qry_1 = Book.query.get(temp['book_id'])
                qry_2 = User.query.get(temp['user_id'])

                temp['book'] = marshal(qry_1, Book.response_field)
                temp['user'] = marshal(qry_2, User.response_field)

                return temp, 200, {'Content-Type': 'application/json'}

            return {'status': 'NOT_FOUND', 'message': 'Book not found'}, 404, {'Content-Type': 'application/json'}


    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        
        parser.add_argument('book_id', type=int, location='json', required=True)
        parser.add_argument('user_id', type=int, location='json', required=True)

        args = parser.parse_args()

        qry_1 = Book.query.get(args['book_id'])
        qry_2 = User.query.get(args['user_id'])

        if qry_1 is None or qry_2 is None:
            return {"Message": "book id or user id not found"}, 404, {'Content-Type': 'application/json'}

        return_date = "2019-02-23"
        post_by = get_jwt_claims()['client_id']
        rent = Rent(None, args['book_id'], args['user_id'], return_date, post_by)

        db.session.add(rent)
        db.session.commit()

        temp = marshal(rent, Rent.response_field)
        temp['user'] = marshal(qry_2, User.response_field)
        temp['book'] = marshal(qry_1, Book.response_field)

        return temp, 200, {'Content-Type': 'application/json'}

api.add_resource(RentResource, '', '/<int:id>')