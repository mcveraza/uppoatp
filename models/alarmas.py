from utils.db import db
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from config import MAILPASSW, MAILADDR

class Alarmas(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    cod_deposito = db.Column(db.String(255))
    cod_parte = db.Column(db.String(255))
    fecha = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    usuario = db.Column(db.String(255))
    mensaje = db.Column(db.String(255))
    estado = db.Column(db.String(255))

    #constructor
    def __init__(self, cod_deposito,cod_parte, usuario, mensaje,estado):
        self.cod_deposito=cod_deposito
        self.cod_parte=cod_parte
        self.usuario=usuario
        self.mensaje=mensaje
        self.estado=estado

    def to_json(self):
        return dict(
            id=self.id,
            cod_deposito=self.cod_deposito,
            cod_parte=self.cod_parte,
            usuario=self.usuario,
            fecha=self.fecha,
            mensaje=self.mensaje,
            estado=self.estado
            )

    def enviar_mail(self, mensaje, to_addr):
       print('enviar_mail')
       msg = MIMEMultipart()
       message = mensaje
 
       # setup the parameters of the message
       msg['From'] = "poaTP@up"
       msg['To'] = to_addr
       msg['Subject'] = "Alarma TP POA"
 
       # add in the message body
       msg.attach(MIMEText(message, 'plain'))
 
       #create server
       server = smtplib.SMTP('smtp.gmail.com')
 
       server.starttls()
 
       # Login Credentials for sending the mail
       print('antes login')
       server.login(MAILADDR,MAILPASSW)
       print('despues login')
       # send the message via the server.
       server.sendmail(msg['From'], msg['To'], msg.as_string())
       server.quit()
       print ("successfully sent email to %s:" % (msg['To']))


#crea todas las tablas de las clases
db.create_all