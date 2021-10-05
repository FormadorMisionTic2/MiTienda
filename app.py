import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import render_template, request, redirect, url_for, session
from flask_login import current_user, login_user, login_required, LoginManager, logout_user
from urllib.parse import urlparse
import redis
import json
from flask_session import Session

login_manager = LoginManager()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://viutzficoufmpa:c0d7d5f9df168feff12131f3352922560adbb1250a644651b2cc28442e06de2b@ec2-54-156-60-12.compute-1.amazonaws.com:5432/d7h26gu4vod24h'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(32)

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url('redis://:p70f7a0d0361fc515e57528b832a4e7010b8b4d96a966c4cd2680a0b9be3dc3d1@ec2-52-5-85-232.compute-1.amazonaws.com:7870')

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager.init_app(app)
login_manager.login_view = "login"
server_session = Session(app)

from models.rol import Rol
from models.usuario import Usuario
from models.producto import Producto
from forms import LoginForm

@app.route("/")
def index():
    productos = Producto.get_all()
    return render_template("index.html",products=productos)

@app.route("/register", methods=["GET","POST"])
def register():
    if(request.method == "GET"):
        return render_template("registro.html", wrongpassword=False)
    else:
        username = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if(password == confirm_password):
            rol = Rol.get_nombre("client")
            user = Usuario(username, password, rol)
            user.create()
            return redirect(url_for("login"))
        else:
            return render_template("registro.html", wrongpassword=True)

@app.route("/login", methods=["GET","POST"])
def login():
    # if(request.method == "GET"):
    #     return render_template("login.html", wrongCredentials=False)
    # else:
    #     username = request.form["email"]
    #     password = request.form["password"]
    #     valida_usuario = Usuario.login(username, password)
    #     if(valida_usuario):
    #         return redirect(url_for("index"))
    #     else:
    #         return render_template("login.html", wrongCredentials=True)
    
    form = LoginForm()
    if form.validate_on_submit():
        valida_usuario = Usuario.login(form.email.data, form.password.data)
        if(valida_usuario):
            user = Usuario.get_email(form.email.data)
            login_user(user)
            
            return redirect(url_for("index"))
    
    return render_template("login_form.html", form=form)

@app.route("/carrito")
@login_required
def carrito():
    return render_template("carrito.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/add/<string:id>")
@login_required
def add_product(id):
    if('cart' in session):
        carrito = session['cart']
        carrito.append(id)
        session['cart'] = carrito
    else:
        session['cart'] = [id]
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=False)