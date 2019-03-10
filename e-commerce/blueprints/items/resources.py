import logging, json
from flask_restful import Resource, Api, reqparse, abort, marshal
from flask import Blueprint, Flask, request
from . import *
from blueprints import db
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_item = Blueprint('item', __name__)
api = Api(bp_item)

class UserItemResource(Resource):
    @jwt_required
    def get(self, id=None):
        if id is None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=5)
            parser.add_argument('negara', location='args')
            parser.add_argument('nama', location='args')
            parser.add_argument('kategori', location='args')
            args = parser.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']  
            
            qry = Item.query

            if args['negara'] is not None:
                qry = qry.filter_by(negara=args['negara'])
            if args['nama'] is not None:
                qry = qry.filter(Item.kategori.like("%"+args['nama']+"%"))
            if args['kategori'] is not None:
                qry = qry.filter_by(kategori=args['kategori'])


            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Item.response_field))
            return rows, 200, {'Content-Type': 'application/json'}

        else:
            qry = Item.query.get(id)
            if qry is not None:
                return marshal(qry, Item.response_field), 200, {'Content-Type': 'application/json'}
            return {'status': 'NOT_FOUND', 'message': 'Item not found'}, 404, {'Content-Type': 'application/json'}


    @jwt_required
    def post(self):
        if get_jwt_claims()['status'] == 'admin':
            parser = reqparse.RequestParser()
            parser.add_argument('negara', location='json', required=True)
            parser.add_argument('nama', location='json', required=True)
            parser.add_argument('kategori', location='json', required=True)
            parser.add_argument('deskripsi', location='json', required=True)
            parser.add_argument('old_price', type=int, location='json', required=True)
            parser.add_argument('new_price', type=int, location='json', required=True)
            parser.add_argument('qty', type=int, location='json', required=True)
            args = parser.parse_args()

            item = Item(None, args['negara'], args['nama'], args['kategori'], args['deskripsi'], args['old_price'], args['new_price'], args['qty'])
            db.session.add(item)
            db.session.commit()

            if item is not None:
                return marshal(item, Item.response_field), 200, {'Content-Type': 'application/json'}
            return {'status': 'NOT_FOUND', 'message': 'Item not found'}, 404, {'Content-Type': 'application/json'}


    @jwt_required
    def patch(self, id):
        if get_jwt_claims()['status'] == 'admin':
            parser = reqparse.RequestParser()
            parser.add_argument('negara', location='json', required=True)
            parser.add_argument('nama', location='json', required=True)
            parser.add_argument('kategori', location='json', required=True)
            parser.add_argument('deskripsi', location='json', required=True)
            parser.add_argument('old_price', type=int, location='json', required=True)
            parser.add_argument('new_price', type=int, location='json', required=True)
            parser.add_argument('qty', type=int, location='json')
            args = parser.parse_args()

            qry = Item.query.get(id)
            qry.negara = args['negara']
            qry.nama = args['nama']
            qry.kategori = args['kategori']
            qry.deskripsi = args['deskripsi']
            qry.old_price = args['old_price']
            qry.new_price = args['new_price']
            qry.qty = args['qty']

            db.session.commit()

            if qry is not None:
                return marshal(qry, Item.response_field), 200, {'Content-Type': 'application/json'}
            return {'status': 'NOT_FOUND', 'message': 'Item not found'}, 404, {'Content-Type': 'application/json'}


    @jwt_required
    def delete(self, id):
        if get_jwt_claims()['status'] == 'admin':
            qry = Item.query.get(id)
            if qry is not None:
                db.session.delete(qry)
                db.session.commit()
                return "deleted", 200
            return {'status': 'NOT_FOUND', 'message': 'Item not found'}, 404, {'Content-Type': 'application/json'}


class PublicItemResource(Resource):

    def get(self, id=None):
        if id is None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=5)
            parser.add_argument('negara', location='args')
            parser.add_argument('nama', location='args')
            parser.add_argument('kategori', location='args')
            args = parser.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']  
            
            qry = Item.query

            if args['negara'] is not None:
                qry = qry.filter_by(negara=args['negara'])
            if args['nama'] is not None:
                qry = qry.filter(Item.kategori.like("%"+args['nama']+"%"))
            if args['kategori'] is not None:
                qry = qry.filter_by(kategori=args['kategori'])

            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Item.response_field))
            return rows, 200, {'Content-Type': 'application/json'}

        else:
            qry = Item.query.get(id)
            if qry is not None:
                return marshal(qry, Item.response_field), 200, {'Content-Type': 'application/json'}
            return {'status': 'NOT_FOUND', 'message': 'Item not found'}, 404, {'Content-Type': 'application/json'}


api.add_resource(UserItemResource, '/users/items', '/users/items/<int:id>')
api.add_resource(PublicItemResource, '/public/items', '/public/items/<int:id>')