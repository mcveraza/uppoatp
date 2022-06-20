from email import utils
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from utils.db import db
from models.roles import Roles

#para separar en modulos las aplicaciones
roles = Blueprint('roles',__name__)

@roles.route('/roles', methods=["GET"])
def get():
    qobj = Roles.query.all()
    return qobj.to_json()


@roles.route('/roles', methods=['POST'])
def create_lab():
     print(request)
     print(request.json)
     if request.method == 'POST':
      codigo = request.json['codigo']
      descripcion = request.json['descripcion']
      try:
       new_objc = Roles(codigo, descripcion)
       db.session.add(new_objc)
       db.session.commit()
       return new_objc.to_json() , 200
      except Exception as ex:
       return jsonify({"error": "Datos incorrectos",}), 400
     else:
      return jsonify({"error": "Recurso no disponible",}), 404