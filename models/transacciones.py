from utils.db import db
import datetime

class Transacciones(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    tipo = db.Column(db.String(255))
    fecha = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    cod_deposito = db.Column(db.String(255))
    cod_labo = db.Column(db.String(255))
    cod_parte = db.Column(db.String(255))
    cantidad = db.Column(db.Float)
    cantidad_des = db.Column(db.Float)
    cantidad_util = db.Column(db.Float)

    #constructor
    def __init__(self, tipo, cod_deposito,cod_labo,cod_parte,cantidad,cantidad_des,cantidad_util):
        self.tipo = tipo
        self.cod_deposito=cod_deposito
        self.cod_labo=cod_labo
        self.cod_parte=cod_parte
        self.cantidad=cantidad
        self.cantidad_des=cantidad_des
        self.cantidad_util=cantidad_util


    def to_json(self):
        return dict(
            id=self.id,
            tipo=self.tipo,
            cod_deposito=self.cod_deposito,
            cod_labo=self.cod_labo,
            cod_parte=self.cod_parte,
            cantidad=self.cantidad,
            cantidad_des=self.cantidad_des,
            cantidad_util=self.cantidad_util
            )

#crea todas las tablas de las clases
db.create_all