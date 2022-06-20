from email import utils
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from utils.db import db
from models.stock import Stock
from sqlalchemy import func, text, select, and_, join

#para separar en modulos las aplicaciones
stock = Blueprint('stock',__name__)


@stock.route('/stock', methods=["GET"])
def getStock():
    #stk = Stock.query.all()
    stmt = select([Stock.id, Stock.cod_deposito, Stock.cod_parte, Stock.cantidad, Stock.capacidad_limite, ((Stock.cantidad / Stock.capacidad_limite) * 100 ).label('capacidad_actual')])
    stock_result = db.session.execute(stmt).fetchall()
    print(stock_result)
    return render_template('stock.html', stock = stock_result)

    
    
    
@stock.route('/stock', methods=['POST'])
def create():
     cod_deposito,cod_parte,cantidad, cap_lim
     cod_deposito = request.json['cod_deposito']
     cod_parte = request.json['cod_parte']
     cantidad = request.json['cantidad']
     cap_lim = request.json['cap_lim']
     new_object = Stock(cod_deposito, cod_parte, cantidad, cap_lim)
     db.session.add(new_object)
     db.session.commit()
     return new_object.to_json()

@stock.route('/stock/<id>', methods=["GET"])
def get(id):
    qobj = Stock.query.get(id)
    return qobj.to_json()

@stock.route('/stock/<id>', methods=["POST"])
def update(id):
    qobj = Stock.query.get(id)
    cantidad = request.json['cantidad']
    qobj.cantidad = cantidad
    db.session.commit()
    return qobj.to_json()