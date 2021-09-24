from app import database

class Producto(database.Model):
    
    __tablename__ = 'productos'
    
    id = database.Column(database.Integer, primary_key=True)
    nombre = database.Column(database.String, nullable=False)
    descripcion = database.Column(database.String, nullable=False)
    precio = database.Column(database.Float, nullable=False)
    imagen = database.Column(database.String, nullable=True)
    
    def __str__(self):
        return f"<Producto {self.id} {self.nombre} {self.descripcion} {self.precio} {self.imagen}>"
    
    @staticmethod
    def get_all():
        return Producto.query.all()