import random, logging
from flask_restful import fields
from blueprints import db

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    negara = db.Column(db.String(255))
    nama = db.Column(db.String(255))
    kategori = db.Column(db.String(255))
    deskripsi = db.Column(db.String(255))
    old_price = db.Column(db.Integer)
    new_price = db.Column(db.Integer)
    qty = db.Column(db.Integer)

    response_field = {
        'id': fields.Integer,
        'negara' : fields.String,
        'nama': fields.String,
        'kategori': fields.String,
        'deskripsi': fields.String,
        'old_price': fields.Integer,
        'new_price' : fields.Integer,
        'qty' : fields.Integer
    }

    def __init__(self, id, negara, nama, kategori, deskripsi, old_price, new_price, qty):
        self.id = id
        self.negara = negara
        self.nama = nama
        self.kategori = kategori
        self.deskripsi = deskripsi
        self.old_price = old_price
        self.new_price = new_price
        self.qty = qty

    def __repr__(self):
        return f'<Item {self.id}>'


db.create_all()