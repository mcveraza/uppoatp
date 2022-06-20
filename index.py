#archivo que arranca la aplicacion
from app import app
from utils.db import db
import config

#source venv/Scripts/activate

with app.app_context():
    db.create_all

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=3000,debug=True)