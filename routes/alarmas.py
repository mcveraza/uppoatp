from email import utils
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from utils.db import db
#importa la clase Alarmas
from models.alarmas import Alarmas
from flask_marshmallow import Marshmallow


#para separar en modulos las aplicaciones
alarmas = Blueprint('alarmas',__name__)


ma = Marshmallow(alarmas)

class AlarmasSchema(ma.Schema):
    class Meta:
        fields=('id', 'cod_deposito', 'cod_parte', 'usuario','mensaje','estado')

alarma_schema=AlarmasSchema()
alarma_schema=AlarmasSchema(many=True)

@alarmas.route('/alarmas', methods=["GET"])
def getAlarmas():
    obj = Alarmas.query.all()
    print(obj)
    return render_template('alarmas.html', alarmas = obj)
    
    
@alarmas.route('/alarmas', methods=['POST'])
def create_alarmas():
     cod_deposito = request.json['cod_deposito']
     cod_parte = request.json['cod_parte']
     usuario = request.json['usuario']
     mensaje = request.json['mensaje']
     estado = request.json['estado']
     new_object = Alarmas(cod_deposito, cod_parte, usuario, mensaje, estado)
     db.session.add(new_object)
     db.session.commit()
     return new_object.to_json()

@alarmas.route('/alarmas/<id>', methods=["GET"])
def get(id):
    qobj = Alarmas.query.get(id)
    return qobj.to_json()

@alarmas.route('/alarmas/<id>', methods=["POST"])
def update(id):
    qobj = Alarmas.query.get(id)
    estado = request.json['estado']
    qobj.estado = estado
    db.session.commit()
    return qobj.to_json()