from flask import Flask, request, jsonify, render_template, redirect, url_for
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy

# Inicializa la aplicación Flask
app = Flask(__name__)

"""
Documentación de Flask SQLAlchemy
https://pythonbasics.org/flask-sqlalchemy/
"""
# Configura la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa SQLAlchemy con la aplicación Flask
db = SQLAlchemy(app)

# Define el modelo de datos para la tabla 'Usuarios'
class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.Integer, unique=True, nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(11), unique=True, nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, cedula, nombre, apellido, telefono, correo):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.correo = correo

"""
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
https://flask.palletsprojects.com/en/3.0.x/
https://flask-sqlalchemy.palletsprojects.com/en/2.x/
"""

@app.route('/')
def index():
    """
    .session.add
    .session.delete
    .query.all ()
    """
    return render_template('index.html', usuarios=Usuarios.query.all())

# Ruta para crear un nuevo usuario
@app.route('/formulario/registro', methods=['POST'])
def crearusuarios():
    if request.method == 'POST':
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        correo = request.form['correo']

        nuevo_usuario = Usuarios(
            cedula = cedula, 
            nombre = nombre, 
            apellido = apellido,
            telefono = telefono,
            correo = correo)
        
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            return redirect(url_for('index'))
        except IntegrityError:
            db.session.rollback()
            return 'Error: El usuario con esa cédula, teléfono o correo ya existe'
        except Exception as e:
            db.session.rollback()
            return f'Error: {str(e)}'

# Ruta para eliminar un usuario
@app.route('/formulario/eliminar/usuarios/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    if request.form.get('_method') == 'DELETE':
        usuario = Usuarios.query.get_or_404(id)  # Obtiene el usuario por id o devuelve un 404 si no existe
        db.session.delete(usuario)  # Elimina el usuario de la sesión
        db.session.commit()  # Guarda los cambios en la base de datos
        return redirect(url_for('index'))

# Punto de entrada 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True, port = 4000)