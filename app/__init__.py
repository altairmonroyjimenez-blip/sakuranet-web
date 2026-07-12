from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        from app import models          # registra los modelos ante SQLAlchemy
        from app.routes import registrar_rutas
        registrar_rutas(app)

    return app