from email import utils
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from utils.db import db
from models.tipo_partes import Tipo_partes

#para separar en modulos las aplicaciones
tipo_partes = Blueprint('tipo_partes',__name__)

@tipo_partes.route('/tipo_partes', methods=["GET"])
def get():
    qobj = Roles.query.all()
    return qobj.to_json()


@tipo_partes.route('/tipo_partes', methods=['POST'])
def create_lab():
     print(request)
     print(request.json)
     if request.method == 'POST':
      codigo = request.json['codigo']
      descripcion = request.json['descripcion']
      try:
       new_objc = Tipo_partes(codigo, descripcion)
       db.session.add(new_objc)
       db.session.commit()
       return new_objc.to_json() , 200
      except Exception as ex:
       return jsonify({"error": "Datos incorrectos",}), 400
     else:
      return jsonify({"error": "Recurso no disponible",}), 404