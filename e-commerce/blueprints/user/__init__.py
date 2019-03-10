import random, logging
from flask_restful import fields
from blueprints import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50))
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    status = db.Column(db.String(255))

    response_field = {
        'id': fields.Integer,
        'email': fields.String,
        'username': fields.String,
        'password': fields.String,
        'status' : fields.String
    }

    def __init__(self, id, email, username, password, status):
        self.id = id
        self.email = email
        self.username = username
        self.password = password
        self.status = status

    def __repr__(self):
        return f'<User {self.id}>'


db.create_all()