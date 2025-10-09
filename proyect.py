from flask import Flask, render_template, session, request, redirect, url_for
from datetime import timedelta
import json
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'
app.permanent_session_lifetime = timedelta(days=30)

# Archivo para guardar usuarios
USUARIOS_FILE = 'usuarios.json'

def cargar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, 'r') as f:
            return json.load(f)
    return {}

def guardar_usuarios(usuarios):
    with open(USUARIOS_FILE, 'w') as f:
        json.dump(usuarios, f)

USUARIOS_REGISTRADOS = cargar_usuarios()

# Ruta raíz que abre NazProyect
@app.route('/')
def index():
    return render_template('NazProyect.html')

# Ruta para formulario de registro
@app.route('/formulario')
def formulario():
    return render_template('formulario.html')

# Ruta para procesar registro
@app.route('/registro', methods=['POST'])
def registro():
    email = request.form.get('email')
    password = request.form.get('password')
    nombre = request.form.get('nombre')
    if email and password and nombre:
        USUARIOS_REGISTRADOS[email] = {'password': password, 'nombre': nombre}
        guardar_usuarios(USUARIOS_REGISTRADOS)
    return redirect(url_for('iniciar'))

# Ruta para login
@app.route('/iniciar')
def iniciar():
    return render_template('iniciar.html')

# Ruta para procesar login
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if email in USUARIOS_REGISTRADOS and USUARIOS_REGISTRADOS[email]['password'] == password:
        session.permanent = True
        session['logged_in'] = True
        session['user_name'] = USUARIOS_REGISTRADOS[email]['nombre']
        return redirect(url_for('index'))
    else:
        return render_template('iniciar.html', error='Email o contraseña incorrectos')

def login_required(f):
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Ruta para "Acerca de"
@app.route('/acerca')
@login_required
def acerca():
    return render_template('acerca.html')

# Ruta para carros
@app.route('/carros')
@login_required
def carros():
    return render_template('carros.html')

# Ruta para maravillas
@app.route('/maravillas')
@login_required
def maravillas():
    return render_template('maravillas.html')

# Ruta para animales
@app.route('/animales')
@login_required
def animales():
    return render_template('base.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('iniciar'))

if __name__ == '__main__':
    app.run(debug=True)