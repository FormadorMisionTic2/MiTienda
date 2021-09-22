from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://viutzficoufmpa:c0d7d5f9df168feff12131f3352922560adbb1250a644651b2cc28442e06de2b@ec2-54-156-60-12.compute-1.amazonaws.com:5432/d7h26gu4vod24h'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(app)

from models.usuario import Usuario

@app.route("/")
def hello():
    correos = ''
    usuarios = Usuario.get_all()
    for user in usuarios:
        correos += user.email + ' '
        print(user.email)
        
    return Usuario.get_id().email
