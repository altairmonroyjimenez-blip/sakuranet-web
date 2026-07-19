from flask import Blueprint, render_template, jsonify, request
from app.models.producto import Producto
from app.models.categoria import Categoria
from app.models.paquete_internet import PaqueteInternet
from app.models.streaming import Streaming
from app.models.producto_destacado import ProductoDestacado

main_bp = Blueprint("main", __name__)

@main_bp.route('/internet')
def internet():
    paquetes = PaqueteInternet.query.filter_by(estado=True).order_by(PaqueteInternet.precio.asc()).all()
    return render_template('internet.html', paquetes=paquetes)

@main_bp.route('/api/buscar')
def api_buscar():
    texto = request.args.get('q', '').strip()
    categoria_id = request.args.get('categoria_id', type=int)

    consulta = Producto.query.filter_by(activo=True)

    if categoria_id:
        consulta = consulta.filter_by(id_categoria=categoria_id)

    if texto:
        consulta = consulta.filter(Producto.nombre.ilike(f'%{texto}%'))

    productos = consulta.all()

    return jsonify([
        {
            "id": p.id_producto,
            "nombre": p.nombre,
            "precio": float(p.precio),
            "imagen": p.imagen_sin_fondo,
            "id_categoria": p.id_categoria
        }
        for p in productos
    ])


@main_bp.route("/")
def inicio():
    destacados = (
        ProductoDestacado.query
        .join(Producto)
        .filter(ProductoDestacado.activo == True, Producto.activo == True)
        .order_by(ProductoDestacado.prioridad.asc())
        .limit(4)
        .all()
    )
    return render_template("index.html", destacados=destacados)


@main_bp.route('/productos')
def productos():
    categorias = Categoria.query.all()

    productos_por_categoria = {
        cat.id_categoria: Producto.query.filter_by(
            activo=True, id_categoria=cat.id_categoria
        ).all()
        for cat in categorias
    }

    return render_template(
        'productos.html',
        categorias=categorias,
        productos_por_categoria=productos_por_categoria
    )


@main_bp.route('/api/productos')
def api_productos():
    categorias = Categoria.query.all()
    data = []

    for cat in categorias:
        productos = Producto.query.filter_by(
            activo=True, id_categoria=cat.id_categoria
        ).all()

        data.append({
            "id_categoria": cat.id_categoria,
            "nombre_categoria": cat.nombre,
            "productos": [
                {
                    "id": p.id_producto,
                    "nombre": p.nombre,
                    "precio": float(p.precio),
                    "imagen": p.imagen_sin_fondo
                }
                for p in productos
            ]
        })

    return jsonify(data)


@main_bp.route('/streaming')
def streaming():
    plataformas = Streaming.query.filter_by(estado=True).order_by(Streaming.precio.asc()).all()
    return render_template('streaming.html', plataformas=plataformas)


@main_bp.route('/contacto')
def contacto():
    return render_template('contacto.html')


@main_bp.route('/papeleria')
def papeleria():
    categoria = Categoria.query.filter_by(nombre='Papelería').first_or_404()
    productos = Producto.query.filter_by(
        activo=True, id_categoria=categoria.id_categoria
    ).all()
    return render_template('categoria_detalle.html', categoria=categoria, productos=productos)


@main_bp.route('/electronica')
def electronica():
    categoria = Categoria.query.filter_by(nombre='Electrónica').first_or_404()
    productos = Producto.query.filter_by(
        activo=True, id_categoria=categoria.id_categoria
    ).all()
    return render_template('categoria_detalle.html', categoria=categoria, productos=productos)

@main_bp.route('/categoria/<int:id_categoria>')
def categoria_detalle(id_categoria):
    categoria = Categoria.query.get_or_404(id_categoria)
    productos = Producto.query.filter_by(
        activo=True, id_categoria=id_categoria
    ).all()

    return render_template(
        'categoria_detalle.html',
        categoria=categoria,
        productos=productos
    )