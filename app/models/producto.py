from app import db
from datetime import datetime

class Producto(db.Model):
    __tablename__ = "productos"

    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(10, 2))
    stock = db.Column(db.Integer)
    imagen_con_fondo = db.Column(db.String(255))
    imagen_sin_fondo = db.Column(db.String(255))
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    id_categoria = db.Column(db.Integer, db.ForeignKey("categorias.id_categoria"))