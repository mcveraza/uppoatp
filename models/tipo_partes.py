import email

from click import password_option
from utils.db import db
import datetime

class Tipo_partes(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    tipo = db.Column(db.String(255))
    porc_limite = db.Column(db.Float)

    #constructor
    def __init__(self, tipo, porc_limite):
        self.tipo=tipo
        self.porc_limite=porc_limite

    def to_json(self):
        return dict(
            id=self.id,
            tipo= self.tipo,
            porc_limite=self.porc_limite
            )

#crea todas las tablas de las clases
db.create_all