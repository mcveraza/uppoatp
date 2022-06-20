from email import utils
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from utils.db import db
from models.laboratorios import Laboratorios
from flask_marshmallow import Marshmallow

#para separar en modulos las aplicaciones
laboratorios = Blueprint('laboratorios',__name__)


ma = Marshmallow(laboratorios)

class LaboratoriosSchema(ma.Schema):
    class Meta:
        fields=('id', 'cod_labo', 'descripcion')

labo_schema=LaboratoriosSchema()
labo_schema=LaboratoriosSchema(many=True)

@laboratorios.route('/laboratorios', methods=["GET"])
def get():
    qobj = Laboratorios.query.all()
    return labo_schema.jsonify(qobj)


@laboratorios.route('/laboratorios', methods=['POST'])
def create_lab():
     print(request)
     print(request.json)
     if request.method == 'POST':
      cod_labo = request.json['cod_labo']
      descripcion = request.json['descripcion']
      try:
       new_lab = Laboratorios(cod_labo, descripcion)
       db.session.add(new_lab)
       db.session.commit()
       return new_lab.to_json() , 200
      except Exception as ex:
       return jsonify({"error": "Datos incorrectos",}), 400
     else:
      return jsonify({"error": "Recurso no disponible",}), 404