import logging, json
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
from flask import Blueprint, Flask, request
from . import *
from blueprints import db
from blueprints.user import User
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims



bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

class CreateTokenResources(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()

        qry = User.query.filter_by(username=args['username']).filter_by(password=args['password']).first()

        if qry is not None:
            token = create_access_token(identity=marshal(qry, User.response_field))
        else:
            return {'status': 'UNAUTHORIZED', 'message': 'invalid username or password'}, 401
        return {'token': token}, 200

api.add_resource(CreateTokenResources, '')