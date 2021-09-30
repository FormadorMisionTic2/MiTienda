from app import database, login_manager
from app import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))

class Usuario(database.Model, UserMixin):
    
    __tablename__ = 'usuarios'
    
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String, nullable=False)
    password = database.Column(database.String, nullable=False)
    rolid = database.Column(database.Integer, database.ForeignKey("rol.id"))
    
    def __init__(self,email,password, rol):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.rolid = rol.id
    
    def __str__(self):
        return f"<Usuario {self.id} {self.email} {self.password} {self.rolid}>"
    
    def create(self):
        database.session.add(self)
        database.session.commit()
    
    @staticmethod
    def get_all():
        return Usuario.query.all()
    
    @staticmethod
    def get_email(email_find):
        return Usuario.query.filter_by(email=email_find).first()
    
    @staticmethod
    def login(email, password):
        success = False
        user = Usuario.get_email(email)
                
        if(user):
            success = bcrypt.check_password_hash(user.password,password)
        
        return success
        