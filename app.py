import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import render_template, request, redirect, url_for, session
from flask_login import current_user, login_user, login_required, LoginManager, logout_user
import redis

login_manager = LoginManager()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://viutzficoufmpa:c0d7d5f9df168feff12131f3352922560adbb1250a644651b2cc28442e06de2b@ec2-54-156-60-12.compute-1.amazonaws.com:5432/d7h26gu4vod24h'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(32)

redistogo_url = os.getenv('REDISTOGO_URL', None)
if redistogo_url == None:
    redis_url = '127.0.0.1:6379'
else:
    redis_url = redistogo_url
    redis_url = redis_url.split('redis://redistogo:')[1]
    redis_url = redis_url.split('/')[0]
    REDIS_PWD, REDIS_HOST = redis_url.split('@', 1)
    redis_url = "%s?password=%s" % (REDIS_HOST, REDIS_PWD)
session_opts = { 'session.type': 'redis', 'session.url': redis_url, 'session.data_dir': './cache/', 'session.key': 'appname', 'session.auto': True, }
r = redis.Redis(redistogo_url)

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager.init_app(app)
login_manager.login_view = "login"


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
    if(r.get('cart')):
        carrito = r.get('cart')
        carrito.append(id)
        r.set("cart", carrito)
    else:
        r.set("cart", [id])
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=False)