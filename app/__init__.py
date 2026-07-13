import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, 'templates'),
        static_folder=os.path.join(base_dir, 'static')
    )
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'cambia-esto-por-algo-secreto-y-unico'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Debes iniciar sesión para acceder a esta página.'

    with app.app_context():
        from app import models
        from app.models.administrador import Administrador

        @login_manager.user_loader
        def load_user(id_admin):
            return Administrador.query.get(int(id_admin))

        from app.routes import registrar_rutas
        registrar_rutas(app)

    return app