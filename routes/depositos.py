from email import utils
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from utils.db import db
from models.depositos import Depositos

#para separar en modulos las aplicaciones
depositos = Blueprint('depositos',__name__)

@depositos.route('/depositos/<id>', methods=["GET"])
def get():
    qobj = Depositos.query.all()
    return qobj.to_json()

@depositos.route('/depositos/<id>', methods=["POST"])
def update(id):
    qobj = Depositos.query.get(id)
    return qobj.to_json()