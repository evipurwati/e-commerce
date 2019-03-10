import random, logging
from flask_restful import fields
from blueprints import db

class Transaction(db.Model):
    __tablename__ = 'transaction'
    cart_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    nama_depan = db.Column(db.String(200))
    nama_belakang = db.Column(db.String(200))
    alamat = db.Column(db.String(200))
    kota = db.Column(db.String(200))
    kode_pos = db.Column(db.String(200))
    no_hp = db.Column(db.String(200))

    response_field = {
        'cart_id': fields.Integer,
        'user_id': fields.Integer,
        'nama_depan': fields.String,
        'nama_belakang': fields.String,
        'alamat': fields.String,
        'kota': fields.String,
        'kode_pos': fields.String,
        'no_hp': fields.String,
    }

    def __init__(self, cart_id, user_id, nama_depan, nama_belakang, alamat, kota, kode_pos, no_hp):
        self.cart_id = cart_id
        self.user_id = user_id
        self.nama_depan = nama_depan
        self.nama_belakang = nama_belakang
        self.alamat = alamat
        self.kota = kota
        self.kode_pos = kode_pos
        self.no_hp = no_hp

    def __repr__(self):
        return f'<Transaction {self.cart_id}>'


db.create_all()