import email

from click import password_option
from utils.db import db
import datetime

class Roles(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    codigo = db.Column(db.String(255))
    descripcion = db.Column(db.String(255))

    #constructor
    def __init__(self, codigo, descripcion):
        self.codigo=codigo
        self.descripcion=descripcion

    def to_json(self):
        return dict(
            id=self.id,
            codigo= self.codigo,
            descripcion=self.descripcion,
            )

#crea todas las tablas de las clases
db.create_all