from flask import Blueprint, render_template
from app.models.producto import Producto

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def inicio():
    return render_template("index.html")

@main_bp.route('/productos')
def productos():
    lista_productos = Producto.query.filter_by(activo=True).all()
    return render_template('productos.html', productos=lista_productos)

@main_bp.route('/internet')
def internet():
    return render_template('internet.html')

@main_bp.route('/streaming')
def streaming():
    return render_template('streaming.html')

@main_bp.route('/contacto')
def contacto():
    return render_template('contacto.html')

@main_bp.route('/papeleria')
def papeleria():
    return render_template('papeleria.html')

@main_bp.route('/electronica')
def electronica():
    return render_template('electronica.html')