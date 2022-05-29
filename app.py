# archivo de configuraciones
from flask import Flask
from routes.transacciones import transacciones
from flask_sqlalchemy import SQLAlchemy
from config import DATA_BASE_CONNECTION_URI


app = Flask(__name__)

# sqlAlchemy connection
app.config['SQLALCHEMY_DATABASE_URI']= DATA_BASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

SQLAlchemy(app)

#para flash, permite compartir mensajes entre paginas:
app.secret_key = 'mysecret'

app.register_blueprint(transacciones)

