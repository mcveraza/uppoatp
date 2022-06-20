# archivo de configuraciones
from flask import Flask
from routes.transacciones import transacciones
from routes.usuarios import usuarios
from routes.stock import stock
from routes.alarmas import alarmas
from routes.roles import roles
from routes.partes import partes
from routes.tipo_partes import tipo_partes
from routes.laboratorios import laboratorios
from flask_sqlalchemy import SQLAlchemy
from config import DATA_BASE_CONNECTION_URI
from flask_login import LoginManager, login_user, logout_user, login_required


app = Flask(__name__)

login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return usuarios.get_by_id(id)

# sqlAlchemy connection

app.config['SQLALCHEMY_DATABASE_URI']= DATA_BASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLAlchemy(app)

#para flash, permite compartir mensajes entre paginas:
app.secret_key = 'mysecret'


app.register_blueprint(transacciones)
app.register_blueprint(usuarios)
app.register_blueprint(stock)
app.register_blueprint(alarmas)
app.register_blueprint(roles)
app.register_blueprint(partes)
app.register_blueprint(tipo_partes)
app.register_blueprint(laboratorios)



