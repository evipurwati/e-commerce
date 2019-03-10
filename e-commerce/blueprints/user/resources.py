import logging, json
from flask_restful import Resource, Api, reqparse, abort, marshal
from flask import Blueprint, Flask, request
from . import *
from blueprints import db
# from blueprints.client import Client
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_user = Blueprint('user', __name__)
api = Api(bp_user)

class UserResource(Resource):
    # @jwt_required
    def get(self, id=None):
        if id is None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=5)
            parser.add_argument('username', location='args')
            args = parser.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']  
            
            qry = User.query
            if args['username'] is not None:
                qry = qry.filter(User.username.like("%"+args['username']+"%"))

            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, User.response_field))
            return rows, 200, {'Content-Type': 'application/json'}

        else:
            qry = User.query.get(id)
            if qry is not None:
                return marshal(qry, User.response_field), 200, {'Content-Type': 'application/json'}
            return {'status': 'NOT_FOUND', 'message': 'User not found'}, 404, {'Content-Type': 'application/json'}


    # @jwt_required
    def post(self):
        # if get_jwt_claims()['status'] == 'admin':
        parser = reqparse.RequestParser()
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('status', location='json', default="user")
        args = parser.parse_args()

        user = User(None, args['email'], args['username'], args['password'], args['status'])
        db.session.add(user)
        db.session.commit()

        if user is not None:
            return marshal(user, User.response_field), 200, {'Content-Type': 'application/json'}
        return {'status': 'NOT_FOUND', 'message': 'Client not found'}, 404, {'Content-Type': 'application/json'}
        # else :
        #     return {'status': 'ACCESS DENIED', 'message': 'ONLY ADMIN ALLOWED!!!!'}, 404, {'Content-Type': 'application/json'}


    # @jwt_required
    def put(self, id):
        # if get_jwt_claims()['status'] == 'admin':
        parser = reqparse.RequestParser()
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        # parser.add_argument('status', location='json', required=True)
        args = parser.parse_args()

        qry = User.query.get(id)
        qry.email = args['email']
        qry.username = args['username']
        qry.password = args['password']
        # qry.status = args['status']

        db.session.commit()

        if qry is not None:
            return marshal(qry, User.response_field), 200, {'Content-Type': 'application/json'}
        return {'status': 'NOT_FOUND', 'message': 'User not found'}, 404, {'Content-Type': 'application/json'}
        # return {'status': 'ACCESS DENIED', 'message': 'ONLY ADMIN ALLOWED!!!!'}, 404, {'Content-Type': 'application/json'}


    # @jwt_required
    def delete(self, id):
        # if get_jwt_claims()['status'] == 'admin':
        qry = User.query.get(id)
        if qry is not None:
            db.session.delete(qry)
            db.session.commit()
            return "deleted", 200
        return {'status': 'NOT_FOUND', 'message': 'User not found'}, 404, {'Content-Type': 'application/json'}
        # return {'status': 'ACCESS DENIED', 'message': 'ONLY ADMIN ALLOWED!!!!'}, 404, {'Content-Type': 'application/json'}

api.add_resource(UserResource, '/users/register', '/users/register/<int:id>')