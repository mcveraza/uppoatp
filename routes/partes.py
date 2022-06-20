from email import utils
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from utils.db import db
from models.partes import Partes
from flask_marshmallow import Marshmallow

#para separar en modulos las aplicaciones
partes = Blueprint('partes',__name__)

ma = Marshmallow(partes)

class PartesSchema(ma.Schema):
    class Meta:
        fields=('id', 'cod_parte', 'descripcion','tipo_parte')

parte_schema=PartesSchema()
parte_schema=PartesSchema(many=True)


@partes.route('/partes', methods=["GET"])
def get():
    qobj = Partes.query.all()
    return parte_schema.jsonify(qobj)


@partes.route('/partes', methods=['POST'])
def create_lab():
     print(request)
     print(request.json)
     if request.method == 'POST':
      cod_parte = request.json['cod_parte']
      descripcion = request.json['descripcion']
      tipo_parte = request.json['tipo_parte']
      try:
       new_objc = Partes(cod_parte, tipo_parte, descripcion)
       db.session.add(new_objc)
       db.session.commit()
       return new_objc.to_json() , 200
      except Exception as ex:
       return jsonify({"error": "Datos incorrectos",}), 400
     else:
      return jsonify({"error": "Recurso no disponible",}), 404