from utils.db import db
import datetime

class Laboratorios(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    cod_labo = db.Column(db.String(255))
    descripcion = db.Column(db.String(255))

    #constructor
    def __init__(self, cod_labo, descripcion):
        self.cod_labo=cod_labo
        self.descripcion=descripcion

    def to_json(self):
        return dict(
            id=self.id,
            cod_labo=self.cod_labo,
            decripcion=self.descripcion
            )

#crea todas las tablas de las clases
db.create_all