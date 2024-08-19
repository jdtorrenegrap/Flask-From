from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicializa la aplicación Flask
app = Flask(__name__)

# Configura la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datos.db'  # Establece la URI de la base de datos SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactiva el seguimiento de modificaciones de SQLAlchemy

# Inicializa SQLAlchemy con la aplicación Flask
db = SQLAlchemy(app)

# Define el modelo de datos para la tabla 'Usuarios'
class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Columna 'id' como clave primaria
    cedula = db.Column(db.Integer, unique=True, nullable=False)  # Columna 'cedula' única y no nula
    nombre = db.Column(db.String(50), nullable=False)  # Columna 'nombre' no nula
    apellido = db.Column(db.String(50), nullable=False)  # Columna 'apellido' no nula
    telefono = db.Column(db.String(11), unique=True, nullable=False)  # Columna 'telefono' única y no nula
    correo = db.Column(db.String(120), unique=True, nullable=False)  # Columna 'correo' única y no nula

    def __init__(self, cedula, nombre, apellido, telefono, correo):
        # Constructor para inicializar los atributos del modelo de dato
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.correo = correo

# Punto de entrada
if __name__ == "__main__":
    db.create_all()  # Crea todas las tablas en la base de datos