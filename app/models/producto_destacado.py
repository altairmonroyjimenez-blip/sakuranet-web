from app import db
from datetime import datetime

class ProductoDestacado(db.Model):
    __tablename__ = "productos_destacados"

    id_destacado = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'))
    prioridad = db.Column(db.Integer, default=0)
    activo = db.Column(db.Boolean, default=True)
    fecha_asignado = db.Column(db.DateTime, default=datetime.utcnow)

    producto = db.relationship('Producto')