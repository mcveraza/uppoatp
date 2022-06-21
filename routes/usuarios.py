from email import utils
from flask import Blueprint, Response, jsonify, render_template, request, redirect, url_for, flash
from utils.db import db
from models.usuarios import Usuarios
from sqlalchemy import text, select, and_, join
from werkzeug.security import generate_password_hash
from flask_marshmallow import Marshmallow

#para separar en modulos las aplicaciones
usuarios = Blueprint('usuarios',__name__)

ma = Marshmallow(usuarios)

class UsuariosSchema(ma.Schema):
    class Meta:
        fields=('id', 'codigo', 'nombre', 'email','telefono','password','rol_id')

usuario_schema=UsuariosSchema()
usuario_schema=UsuariosSchema(many=True)



@usuarios.route('/')
def index():
    return redirect(url_for('usuarios.login'))

@classmethod
def get_by_id(self, id):
  qobj = Usuarios.query.get(id)
  return qobj

@usuarios.route('/usuarios', methods=["GET"])
def get():
    try:
     qobj = Usuarios.query.all()
     return usuario_schema.jsonify(qobj), 200
    except Exception as e:
     return jsonify({"Error": "Invalid Request, please try again."})


@usuarios.route('/usuarios/<id>', methods=["GET"])
def update(id):
    qobj = Usuarios.query.get(id)
    return qobj.to_json()
    

@usuarios.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario_login = request.form['inputUser']
        pwd_login= request.form['inputPassword']
        new_user = Usuarios(usuario_login, '', '', '', pwd_login, '')

        #logged_user = ModelUser.login(db, user)
        print('validar si usuario existe')

        stmt = select([Usuarios.id]).where(Usuarios.codigo == usuario_login)
        usr_log_result = db.session.execute(stmt).fetchall()
        if not usr_log_result:
          print('result query is empty')
          flash("No se encontro el usuario")   
          return render_template('auth/login.html') 
        else:   
           #--validar pwd--
           print(usr_log_result)
           resultx = [r[0] for r in usr_log_result]
           idUser = resultx[0]
           print(idUser)
           user_obj = Usuarios.query.get(idUser)
           if user_obj.check_password(user_obj.password, pwd_login):
              print('pwd  OK')
              #login_user(logged_user)
              return redirect(url_for('transacciones.home'))
           else:
             print('Password invalida')
             flash("Invalid Password")  
             return render_template('auth/login.html')            
    else:
        print('NO POST')
        return render_template('auth/login.html')


'''
postman:
  
 POST http://localhost:3000/usuarios 
 body:
{
    "codigo":"USER5",
    "nombre":"Pepito Test",
    "email":"pepito@test.com",
    "telefono":"11322222",
    "password":"54321",
    "rol_id":4
}

'''

@usuarios.route('/usuarios', methods=['POST'])
def create_user():
     print(request)
     print(request.json)
     if request.method == 'POST':
      codigo = request.json['codigo']
      nombre = request.json['nombre']
      email = request.json['email']
      telefono = request.json['telefono']
      password = request.json['password']
      rol_id = request.json['rol_id']
      try:
       new_usr = Usuarios(codigo, nombre, email, telefono, generate_password_hash(password), rol_id)
       db.session.add(new_usr)
       db.session.commit()
       return new_usr.to_json() , 200
      except Exception as ex:
       return jsonify({"error": "Datos de usuario incorrecto",}), 400
     else:
      return jsonify({"error": "Recurso no disponible",}), 404

