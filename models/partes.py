import email

from click import password_option
from utils.db import db
import datetime

class Partes(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    cod_parte = db.Column(db.String(255))
    tipo_parte_id= db.Column(db.Integer)
    descripcion = db.Column(db.String(255))

    #constructor
    def __init__(self, cod_parte, descripcion, tipo_parte_id):
        self.cod_parte=cod_parte
        self.descripcion=descripcion
        self.tipo_parte_id=tipo_parte_id

    def to_json(self):
        return dict(
            id=self.id,
            codigo= self.codigo,
            descripcion=self.descripcion,
            tipo_parte_id=self.tipo_parte_id
            )

#crea todas las tablas de las clases
db.create_all