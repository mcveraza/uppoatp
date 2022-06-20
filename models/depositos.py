from utils.db import db
import datetime

class Depositos(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    cod_deposito = db.Column(db.String(255))
    descripcion = db.Column(db.String(255))

    #constructor
    def __init__(self, cod_deposito, descripcion):
        self.cod_deposito=cod_deposito
        self.descripcion=descripcion

    def to_json(self):
        return dict(
            id=self.id,
            cod_deposito=self.cod_deposito,
            decripcion=self.descripcion
            )

#crea todas las tablas de las clases
db.create_all