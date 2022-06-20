from click import password_option
from utils.db import db
import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class Usuarios(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    codigo = db.Column(db.String(255))
    nombre = db.Column(db.String(255))
    email= db.Column(db.String(255))
    telefono= db.Column(db.String(255))
    password= db.Column(db.String(255))
    rol_id= db.Column(db.Integer)

    #constructor
    def __init__(self, codigo, nombre, email,telefono,password,rol_id):
        self.codigo=codigo
        self.nombre=nombre
        self.email=email
        self.telefono=telefono
        self.password=password
        self.rol_id=rol_id

    def to_json(self):
        return dict(
            id=self.id,
            codigo= self.codigo,
            nombre=self.nombre,
            email=self.email,
            telefono=self.telefono,
            password=self.password,
            rol_id=self.rol_id
            )

    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)

#crea todas las tablas de las clases
db.create_all