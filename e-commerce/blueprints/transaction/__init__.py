import random, logging
from flask_restful import fields
from blueprints import db

class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.String(200))
    user_id = db.Column(db.String(200))
    return_date = db.Column(db.String(200))
    post_by = db.Column(db.String(200))

    response_field = {
        'id': fields.Integer,
        'book_id': fields.String,
        'user_id': fields.String,
        'return_date': fields.String,
        'post_by': fields.String
    }

    def __init__(self, id, book_id, user_id, return_date, post_by):
        self.id = id
        self.book_id = book_id
        self.user_id = user_id
        self.return_date = return_date
        self.post_by = post_by

    def __repr__(self):
        return f'<Rent {self.id}>'


db.create_all()