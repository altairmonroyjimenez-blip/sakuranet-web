from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Administrador(UserMixin, db.Model):
    __tablename__ = "administradores"

    id_admin = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(150))
    rol = db.Column(db.String(50))

    # Flask-Login necesita un método get_id() -> lo da UserMixin,
    # pero usa self.id por defecto; como tu PK se llama id_admin,
    # lo sobreescribimos:
    def get_id(self):
        return str(self.id_admin)

    def set_password(self, password_plano):
        self.password = generate_password_hash(password_plano)

    def check_password(self, password_plano):
        return check_password_hash(self.password, password_plano)