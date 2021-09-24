from app import database

class Rol(database.Model):
    __tablename__ = 'rol'
    
    id = database.Column(database.Integer, primary_key=True)
    nombre = database.Column(database.String, nullable=False)
    descripcion = database.Column(database.String, nullable=True)
    usuarios = database.relationship("Usuario", backref="rol",lazy=True)
    
    @staticmethod
    def get_id(id):
        return Rol.query.filter_by(id=id).first()
    
    @staticmethod
    def get_nombre(nombre_buscar):
        return Rol.query.filter_by(nombre=nombre_buscar).first()