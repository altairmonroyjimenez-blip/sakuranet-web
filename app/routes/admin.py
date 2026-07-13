from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models.producto import Producto
from app.models.categoria import Categoria
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route('/')
@login_required
def dashboard():
    total_productos = Producto.query.count()
    total_activos = Producto.query.filter_by(activo=True).count()
    return render_template('admin/dashboard.html',
                            total_productos=total_productos,
                            total_activos=total_activos)


@admin_bp.route('/productos')
@login_required
def productos_lista():
    productos = Producto.query.order_by(Producto.id_producto.desc()).all()
    return render_template('admin/productos_lista.html', productos=productos)


@admin_bp.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
def producto_nuevo():
    categorias = Categoria.query.all()

    if request.method == 'POST':
        nombre_imagen = guardar_imagen(request.files.get('imagen'))

        nuevo = Producto(
            nombre=request.form.get('nombre'),
            descripcion=request.form.get('descripcion'),
            precio=request.form.get('precio'),
            stock=request.form.get('stock'),
            imagen_con_fondo=nombre_imagen,
            imagen_sin_fondo=nombre_imagen,
            id_categoria=request.form.get('id_categoria'),
            activo=True
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Producto creado correctamente.', 'success')
        return redirect(url_for('admin.productos_lista'))

    return render_template('admin/producto_form.html', producto=None, categorias=categorias)


@admin_bp.route('/productos/<int:id_producto>/editar', methods=['GET', 'POST'])
@login_required
def producto_editar(id_producto):
    producto = Producto.query.get_or_404(id_producto)
    categorias = Categoria.query.all()

    if request.method == 'POST':
        nombre_imagen = guardar_imagen(request.files.get('imagen'))

        producto.nombre = request.form.get('nombre')
        producto.descripcion = request.form.get('descripcion')
        producto.precio = request.form.get('precio')
        producto.stock = request.form.get('stock')

        if nombre_imagen:
            producto.imagen_con_fondo = nombre_imagen
            producto.imagen_sin_fondo = nombre_imagen

        producto.id_categoria = request.form.get('id_categoria')
        producto.activo = 'activo' in request.form

        db.session.commit()
        flash('Producto actualizado correctamente.', 'success')
        return redirect(url_for('admin.productos_lista'))

    return render_template('admin/producto_form.html', producto=producto, categorias=categorias)

@admin_bp.route('/productos/<int:id_producto>/eliminar', methods=['POST'])
@login_required
def producto_eliminar(id_producto):
    producto = Producto.query.get_or_404(id_producto)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado.', 'success')
    return redirect(url_for('admin.productos_lista'))

def guardar_imagen(archivo):
    if not archivo or archivo.filename == '':
        return None
    extension = secure_filename(archivo.filename).rsplit('.', 1)[-1].lower()
    nombre_unico = f"{uuid.uuid4().hex}.{extension}"
    ruta_completa = os.path.join(current_app.config['UPLOAD_FOLDER'], nombre_unico)
    archivo.save(ruta_completa)
    return nombre_unico