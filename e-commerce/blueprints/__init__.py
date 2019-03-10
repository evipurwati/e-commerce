from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
from time import strftime
import json, logging
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)

# CONNECTION STRING
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@0.0.0.0:3306/ecommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# FOR JWT MANAGER
app.config['JWT_SECRET_KEY'] = '12345678'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

# MIDDLE WARE UNTUK DAPATKAN IDENTITY
@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return identity


db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# initiate flask-restful instance
api = Api(app, catch_all_404s=True)


## MIDDLE WARE
@app.after_request
def after_request(response):
    if request.method == 'GET':
        app.logger.warning("REQUEST_LOG\t%s %s %s %s", response.status_code, request.method, request.url, json.dumps({ 'request': request.args.to_dict(), 'response': json.loads(response.data.decode('utf-8')) }))
    else:
        app.logger.warning("REQUEST_LOG\t%s %s %s %s", response.status_code, request.method, request.url, json.dumps({ 'request': request.get_json(), 'response': json.loads(response.data.decode('utf-8')) }))
    return response

# CALL BLUEPRINT
from blueprints.auth import bp_auth
from blueprints.user.resources import bp_user
from blueprints.items.resources import bp_item
from blueprints.cart.resources import bp_cart

app.register_blueprint(bp_auth, url_prefix='/users/login')
app.register_blueprint(bp_user) 
app.register_blueprint(bp_item)
app.register_blueprint(bp_cart)



db.create_all()
