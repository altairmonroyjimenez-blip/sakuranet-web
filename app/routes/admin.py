from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models.producto import Producto
from app.models.categoria import Categoria
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
from app.models.paquete_internet import PaqueteInternet
from app.models.streaming import Streaming

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


@admin_bp.route('/paquetes')
@login_required
def paquetes_lista():
    paquetes = PaqueteInternet.query.order_by(PaqueteInternet.precio.asc()).all()
    return render_template('admin/paquetes_lista.html', paquetes=paquetes)


@admin_bp.route('/paquetes/nuevo', methods=['GET', 'POST'])
@login_required
def paquete_nuevo():
    if request.method == 'POST':
        nuevo = PaqueteInternet(
            nombre=request.form.get('nombre'),
            velocidad=request.form.get('velocidad'),
            subida=request.form.get('subida'),
            precio=request.form.get('precio'),
            descripcion=request.form.get('descripcion'),
            estado=True
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Paquete creado correctamente.', 'success')
        return redirect(url_for('admin.paquetes_lista'))

    return render_template('admin/paquete_form.html', paquete=None)


@admin_bp.route('/paquetes/<int:id_paquete>/editar', methods=['GET', 'POST'])
@login_required
def paquete_editar(id_paquete):
    paquete = PaqueteInternet.query.get_or_404(id_paquete)

    if request.method == 'POST':
        paquete.nombre = request.form.get('nombre')
        paquete.velocidad = request.form.get('velocidad')
        paquete.subida = request.form.get('subida')
        paquete.precio = request.form.get('precio')
        paquete.descripcion = request.form.get('descripcion')
        paquete.estado = 'estado' in request.form

        db.session.commit()
        flash('Paquete actualizado correctamente.', 'success')
        return redirect(url_for('admin.paquetes_lista'))

    return render_template('admin/paquete_form.html', paquete=paquete)


@admin_bp.route('/paquetes/<int:id_paquete>/eliminar', methods=['POST'])
@login_required
def paquete_eliminar(id_paquete):
    paquete = PaqueteInternet.query.get_or_404(id_paquete)
    db.session.delete(paquete)
    db.session.commit()
    flash('Paquete eliminado.', 'success')
    return redirect(url_for('admin.paquetes_lista'))

@admin_bp.route('/streaming')
@login_required
def streaming_lista():
    plataformas = Streaming.query.order_by(Streaming.precio.asc()).all()
    return render_template('admin/streaming_lista.html', plataformas=plataformas)


@admin_bp.route('/streaming/nuevo', methods=['GET', 'POST'])
@login_required
def streaming_nuevo():
    if request.method == 'POST':
        nombre_imagen = guardar_imagen(request.files.get('imagen'))

        nuevo = Streaming(
            nombre=request.form.get('nombre'),
            precio=request.form.get('precio'),
            descripcion=request.form.get('descripcion'),
            imagen=nombre_imagen,
            estado=True
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Plataforma agregada correctamente.', 'success')
        return redirect(url_for('admin.streaming_lista'))

    return render_template('admin/streaming_form.html', plataforma=None)


@admin_bp.route('/streaming/<int:id_streaming>/editar', methods=['GET', 'POST'])
@login_required
def streaming_editar(id_streaming):
    plataforma = Streaming.query.get_or_404(id_streaming)

    if request.method == 'POST':
        nombre_imagen = guardar_imagen(request.files.get('imagen'))

        plataforma.nombre = request.form.get('nombre')
        plataforma.precio = request.form.get('precio')
        plataforma.descripcion = request.form.get('descripcion')

        if nombre_imagen:
            plataforma.imagen = nombre_imagen

        plataforma.estado = 'estado' in request.form

        db.session.commit()
        flash('Plataforma actualizada correctamente.', 'success')
        return redirect(url_for('admin.streaming_lista'))

    return render_template('admin/streaming_form.html', plataforma=plataforma)


@admin_bp.route('/streaming/<int:id_streaming>/eliminar', methods=['POST'])
@login_required
def streaming_eliminar(id_streaming):
    plataforma = Streaming.query.get_or_404(id_streaming)
    db.session.delete(plataforma)
    db.session.commit()
    flash('Plataforma eliminada.', 'success')
    return redirect(url_for('admin.streaming_lista'))