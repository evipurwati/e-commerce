import random, logging
from flask_restful import fields
from blueprints import db

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    total_harga = db.Column(db.Integer)
    # created_at = db.

    response_field = {
        'id': fields.Integer,
        'user_id' : fields.Integer,
        'item_id' : fields.Integer,
        'total_harga': fields.Integer
        # 'created_at': fields.String
    }

    def __init__(self, id, user_id, item_id, total_harga):
        self.id = id
        self.user_id = user
        self.item_id = id_item
        self.total_harga = total_harga

    def __repr__(self):
        return f'<Cart {self.id}>'


db.create_all()