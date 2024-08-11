from flask import Flask, request, render_template, redirect, url_for
from sqlalchemy.exc import IntegrityError
from models import db, Usuarios

# Inicializa la aplicación Flask
app = Flask(__name__)

# Configura la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa SQLAlchemy con la aplicación Flask
db.init_app(app)

@app.route('/')
def index():
    """
    Ruta principal que muestra todos los usuarios.
    """
    return render_template('index.html', usuarios=Usuarios.query.all())

@app.route('/formulario/registro', methods=['POST'])
def crearusuarios():
    """
    Ruta para crear un nuevo usuario.
    """
    cedula = request.form['cedula']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    telefono = request.form['telefono']
    correo = request.form['correo']

    nuevo_usuario = Usuarios(
        cedula=cedula, 
        nombre=nombre, 
        apellido=apellido,
        telefono=telefono,
        correo=correo
    )
    
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

@app.route('/formulario/eliminar/usuarios/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    """
    Ruta para eliminar un usuario.
    """
    if request.form.get('_method') == 'DELETE':
        usuario = Usuarios.query.get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return redirect(url_for('index'))

# Punto de entrada
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=4000)