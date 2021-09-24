from app import database

class Pedido(database.Model):
    __tablename__ = 'pedido'
    id = database.Column(database.Integer, primary_key=True)
    productoid = database.Column(database.Integer, database.ForeignKey("producto.id"))
    usuarioid = database.Column(database.Integer, database.ForeignKey("usuario.id"))
    
    @staticmethod
    def get_all():
        return Pedido.query.all()