import random, logging
from flask_restful import fields
from blueprints import db

class Cart(db.Model):
    __tablename__ = 'cart'
    transaction_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    qty = db.Column(db.Integer)
    price = db.Column(db.Integer)
    # created_at = db.Column(db.String(200))
    # updated_at = db.Column(db.String(200))

    response_field = {
        'transaction_id': fields.Integer,
        'user_id' : fields.Integer,
        'item_id' : fields.Integer,
        'status' : fields.Boolean,
        'qty': fields.Integer,
        'price' : fields.Integer
        # 'created_at' : fields.String,
        # 'updated_at' : fields.String
    }

    def __init__(self, transaction_id, user_id, item_id, status, qty, price):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.item_id = item_id
        self.status = status
        self.qty = qty
        self.price = price
        # self.created_at = created_at

    def __repr__(self):
        return f'<Cart {self.transaction_id}>'


db.create_all()