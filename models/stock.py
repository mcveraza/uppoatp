from tkinter import Y
from utils.db import db
import datetime

class Stock(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    cod_deposito = db.Column(db.String(255))
    cod_parte = db.Column(db.String(255))
    cantidad = db.Column(db.Float)
    capacidad_limite = db.Column(db.Float)

    #constructor
    def __init__(self, cod_deposito,cod_parte,cantidad, cap_lim):
        self.cod_deposito=cod_deposito
        self.cod_parte=cod_parte
        self.cantidad=cantidad
        self.capacidad_limite = cap_lim

    def to_json(self):
        return dict(
            id=self.id,
            cod_deposito=self.cod_deposito,
            cod_parte=self.cod_parte,
            cantidad=self.cantidad,
            capacidad_limite = self.capacidad_limite
            )

#crea todas las tablas de las clases
db.create_all