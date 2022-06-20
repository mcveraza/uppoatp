from doctest import Example
from email import utils
from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.db import db
#importa la clase Transacciones
from models.transacciones import Transacciones
from models.stock import Stock
from models.alarmas import Alarmas
from models.usuarios import Usuarios
from models.roles import Roles
from models.partes import Partes
from models.tipo_partes import Tipo_partes
from sqlalchemy import text, select, and_, join
import logging
from flask_login import LoginManager, login_user, logout_user, login_required
from sqlalchemy_paginator import Paginator

#para separar en modulos las aplicaciones
transacciones = Blueprint('transacciones',__name__)



@transacciones.route("/home")
#@login_required
def home():
    print('transacciones.home')
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
     
     if tipo == "EGR":
       print('EGRESO')
       #validar egreso de stock --. 
       stmt = select([Stock.id]).where(and_(Stock.cod_deposito == cod_deposito,
                                          Stock.cod_parte == cod_parte
                                          ))
       stock_result = db.session.execute(stmt).fetchall()
       if not stock_result:
          print('result query is empty')
          flash("No hay stock para egresos")    
       else:   
           #--actualizar_stock--
           print(stock_result)
           resultx = [r[0] for r in stock_result]
           idStock = resultx[0]
           print(idStock)
           stock_obj = Stock.query.get(idStock)
           if stock_obj.cantidad >= float(cantidad):
              stock_obj.cantidad = float(stock_obj.cantidad) -  float(cantidad)
              print('stock actualizado')
              #ingresar_trx
              new_transaccion = Transacciones(tipo, cod_deposito, cod_labo, cod_parte, cantidad, cantidad_des, cantidad_util)
              db.session.add(new_transaccion)
              db.session.commit()
              flash("Transaccion de EGRESO creada exitosamente")
              print('trx creada')
             
              #--check_alarma----
              #obtener del tipo de pieza el porcentaje limite
              stmt = select([Tipo_partes.porc_limite]).join(Partes, Partes.tipo_parte_id == Tipo_partes.id).where(Partes.cod_parte == cod_parte)

              p_result = db.session.execute(stmt).fetchall()
              if not p_result:
                print('tipo parte query is empty')
                flash("tipo parte no enconetrada")    
              else:   
                #--verificar porc limite
                print(p_result)
                resultx = [r[0] for r in p_result]
                porc_lim_r = resultx[0]
                print('porc limi parte')
                print(porc_lim_r)
                print('obteniendo porc actual parte en deposito: ')
                print('stock actual')
                print(stock_obj.cantidad)
                print('capacidad limite: ') 
                print(stock_obj.capacidad_limite)
                print('calculando porc_act ')
                porc_act = (float(stock_obj.cantidad) / float(stock_obj.capacidad_limite)) * 100
                print(porc_act)

                if float(porc_act) < float(porc_lim_r):
                #COMENTADO EL IF PARA QUE ENTRE EN ESTA PARTE Y PROBAR ENVIO DE ALARMAS!!!!!!!!!!!!
                #if 1==1:
                  #crear alarma         
                  print('crear alarma')
                  print('obteniendo usuarios')

                  stmt = select([Usuarios.email, Usuarios.codigo, Usuarios.nombre]).join(Roles, Usuarios.rol_id == Roles.id).where(Roles.codigo == "SUPERVISOR")
                  usuarios_alarmas = db.session.execute(stmt).fetchall()
                  if not usuarios_alarmas:
                    print('roles usuarios query is empty')
                    flash("usuarios supervisores no enconetrados")    
                  else:   
                    #--verificar porc limite
                    print(usuarios_alarmas)

                    for r in usuarios_alarmas:
                       email_usuario=r[0]
                       print(email_usuario)
                       cod_usuario = r[1]
                       print(cod_usuario)
                       nombre_usuario = r[2]
                       print(nombre_usuario)
                       #enviar_alarma()
                       mensaje = ('Hola '+nombre_usuario+': El stock para el DEPOSITO: ' + cod_deposito + ' , PARTE: ' + cod_parte + 
                              ' esta por debajo del PORC. LIMITE. Por favor, realizar las acciones correspondientes.' )
                       new_alarma = Alarmas(cod_deposito,cod_parte,cod_usuario, mensaje, "PENDIENTE")
                       try:
                         new_alarma.enviar_mail(mensaje, email_usuario)
                         new_alarma.estado='ENVIADA'
                         db.session.add(new_alarma)
                         db.session.commit()
                         print("enviar alarma")   
                       except Exception as ex:
                        print('error envio mail')
                        print (ex)
                        

           else:
             flash("Cantidad en Stock insuficiente. Transaccion de EGRESO no creada.")     

     else:
       print('INGRESO')
       logging.warning("INGRESO proceso....")
       #trx de INGRESO
       #actualizar stock
       stmt = select([Stock.id]).where(and_(Stock.cod_deposito == cod_deposito,
                                          Stock.cod_parte == cod_parte
                                          ))
       stock_result = db.session.execute(stmt).fetchall()
       
       if not stock_result:
          print('result query stock is empty')
          flash("No hay stock para egresos")    
       else:
          print(stock_result)
          resultx = [r[0] for r in stock_result]
          idStock = resultx[0]
          print(idStock)
          stock_obj = Stock.query.get(idStock)
          stock_obj.cantidad = float(stock_obj.cantidad) +  float(cantidad)
       new_transaccion = Transacciones(tipo, cod_deposito, cod_labo, cod_parte, cantidad, cantidad_des, cantidad_util)
       db.session.add(new_transaccion)
       db.session.commit()
       flash("Transaccion de INGRESO creada exitosamente")
     return redirect(url_for("transacciones.home"))



@transacciones.route('/update/<id>', methods=["GET","POST"])
def update(id):
    q_trx = Transacciones.query.get(id)
    if request.method=="POST":
      q_trx.cantidad_des = request.form["cantidad_des"]
      q_trx.cantidad_util = request.form["cantidad_util"]
      #validar cantidad_des + cantidad_util = cantidad
      db.session.commit()
      flash("Transaccion actualizada exitosamente")
      return redirect(url_for("transacciones.home"))
    return render_template('edit_trx.html', trx = q_trx)


#@API con paginacion
@transacciones.route('/reporte', methods=['GET','POST'], defaults={"page": 1}) 
@transacciones.route('/reporte/<int:page>', methods=['GET', 'POST'])
def reporte(page):
    print('transacciones.route ')
    print(page)
    page = int(page)
    per_page = 5
    
    #trxs = Transacciones.query.all()
    trxs = Transacciones.query.paginate(page,per_page,max_per_page=10,error_out=False)

    return render_template('reporte.html', transacciones = trxs)


