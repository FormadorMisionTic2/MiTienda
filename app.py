from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://viutzficoufmpa:c0d7d5f9df168feff12131f3352922560adbb1250a644651b2cc28442e06de2b@ec2-54-156-60-12.compute-1.amazonaws.com:5432/d7h26gu4vod24h'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from models.rol import Rol
from models.usuario import Usuario
from models.producto import Producto

@app.route("/")
def hello():
    productos = Producto.get_all()
    print(productos)
    return render_template("index.html",products=productos)


@app.route("/login")
def login():
    username = "clienteuno@gmail.com"
    password = "misifu123"
    valida_usuario = Usuario.login(username, password)

    return render_template("login.html")


@app.route("/register")
def register():

    username = "clienteuno@gmail.com"
    password = "misifu123"
    rol = Rol.get_nombre("client")
    user = Usuario(username, password, rol)
    user.create()

    return str()

