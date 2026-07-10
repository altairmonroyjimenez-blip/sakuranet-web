from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/internet')
def internet():
    return render_template('internet.html')

@app.route('/streaming')
def streaming():
    return render_template('streaming.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

# 🔥 Rutas que estaban abajo (las subimos)
@app.route('/papeleria')
def papeleria():
    return render_template('papeleria.html')

@app.route('/electronica')
def electronica():
    return render_template('electronica.html')

if __name__ == "__main__":
    app.run(debug=True)
