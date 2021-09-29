from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import render_template, request, redirect, url_for


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://viutzficoufmpa:c0d7d5f9df168feff12131f3352922560adbb1250a644651b2cc28442e06de2b@ec2-54-156-60-12.compute-1.amazonaws.com:5432/d7h26gu4vod24h'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from models.rol import Rol
from models.usuario import Usuario
from models.producto import Producto

@app.route("/")
def index():
    productos = Producto.get_all()
    print(productos)
    return render_template("index.html",products=productos)


@app.route("/login", methods=["GET","POST"])
def login():
    if(request.method == "GET"):
        return render_template("login.html", wrongCredentials=False)
    else:
        username = request.form["email"]
        password = request.form["password"]
        valida_usuario = Usuario.login(username, password)
        if(valida_usuario):
            return redirect(url_for("index"))
        else:
            return render_template("login.html", wrongCredentials=True)



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

    

