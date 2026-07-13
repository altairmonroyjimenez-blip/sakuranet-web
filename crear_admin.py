from app import create_app, db
from app.models.administrador import Administrador

app = create_app()

with app.app_context():
    existe = Administrador.query.filter_by(usuario='admin').first()
    if existe:
        print("Ya existe un admin con ese usuario.")
    else:
        nuevo_admin = Administrador(
            usuario='admin',
            nombre='Altair Monroy',
            rol='superadmin'
        )
        nuevo_admin.set_password('altair123')
        db.session.add(nuevo_admin)
        db.session.commit()
        print("Administrador creado correctamente.")