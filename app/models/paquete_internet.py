from app import db

class PaqueteInternet(db.Model):
    __tablename__ = "paquetes_internet"

    id_paquete = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    velocidad = db.Column(db.String(50))
    subida = db.Column(db.String(50))
    precio = db.Column(db.Numeric(10, 2))
    descripcion = db.Column(db.Text)
    estado = db.Column(db.Boolean, default=True)