from app import db

class Streaming(db.Model):
    __tablename__ = "streaming"

    id_streaming = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    precio = db.Column(db.Numeric(10, 2))
    descripcion = db.Column(db.Text)
    imagen = db.Column(db.String(255))
    estado = db.Column(db.Boolean, default=True)