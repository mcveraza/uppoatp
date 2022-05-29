from email import utils
from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.db import db
#importa la clase Transacciones
from models.transacciones import Transacciones

#para separar en modulos las aplicaciones
transacciones = Blueprint('transacciones',__name__)

@transacciones.route("/")
def home():
    trxs = Transacciones.query.all()
    return render_template('index.html', transacciones = trxs)

@transacciones.route('/transacciones', methods=['POST'])
def create_transacciones():
     tipo = request.form['tipo']
     cod_deposito = request.form['cod_deposito']
     cod_labo = request.form['cod_labo']
     cod_parte = request.form['cod_parte']
     cantidad = request.form['cantidad']
     cantidad_des = 0
     cantidad_util = 0
     #validar_stock --. Solo si esta ok continuar
     #actualizar_stock
     #check_alarma 
     #ingresar_trx:
     new_transaccion = Transacciones(tipo, cod_deposito, cod_labo, cod_parte, cantidad, cantidad_des, cantidad_util)
     db.session.add(new_transaccion)
     db.session.commit()
     flash("Transaccion creada exitosamente")
     return redirect(url_for("transacciones.home"))

@transacciones.route('/update/<id>', methods=["GET","POST"])
def update(id):
    q_trx = Transacciones.query.get(id)
    if request.method=="POST":
      q_trx.cantidad_des = request.form["cantidad_des"]
      q_trx.cantidad_util = request.form["cantidad_util"]
      #validar cantidad_des + cantidad_util = cantidad
      db.session.commit()
      flash("Transaccion creada exitosamente")
      return redirect(url_for("transacciones.home"))
    return render_template('edit_trx.html', trx = q_trx)

@transacciones.route("/reportes")
def reportes():
    return render_template('reportes.html')


