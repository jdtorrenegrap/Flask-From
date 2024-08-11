from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicializa la aplicación Flask
app = Flask(__name__)

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

# Punto de entrada
if __name__ == "__main__":
    db.create_all()