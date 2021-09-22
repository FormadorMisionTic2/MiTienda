from app import database

class Usuario(database.Model):
    
    __tablename__ = 'usuarios'
    
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String, nullable=False)
    password = database.Column(database.String, nullable=False)
    #nombre = database.Column(database.String(256), nullable=True)
    
    @staticmethod
    def get_all():
        return Usuario.query.all()
    
    @staticmethod
    def get_id():
        return Usuario.query.filter_by(id=7).first()