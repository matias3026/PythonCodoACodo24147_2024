# Importación de módulos necesarios de Flask y MySQL
# paso 1
from flask import Flask, render_template, redirect, request, Response, session, url_for, jsonify
from flask_mysqldb import MySQL, MySQLdb

# Inicialización de la aplicación Flask con las carpetas de plantillas y archivos estáticos
# paso 2
app = Flask(__name__, template_folder='template', static_folder='static')

# Configuración de la conexión a la base de datos MySQL
# paso 3
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cafeteria'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)  # Inicialización de la extensión MySQL con la aplicación Flask

# Ruta principal que redirige a la página de inicio (login)
# paso 4 redigir a ruta del index
@app.route('/')
def home():
    return render_template('index.html')  # Renderiza la plantilla 'index.html'

# Ruta para el panel de administración
@app.route('/admin')
def admin():
    # Verifica si el usuario ha iniciado sesión
    if 'nombre_usuario' not in session:
        return redirect(url_for('login'))  # Si no ha iniciado sesión, redirige al login

    # Conexión a la base de datos y ejecución de consultas
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')  # Obtiene todos los productos
    productos = cur.fetchall()

    cur.execute('SELECT DISTINCT categoria_producto FROM productos')  # Obtiene todas las categorías únicas
    categorias = [row['categoria_producto'] for row in cur.fetchall()]

    cur.close()
    # Renderiza la plantilla 'admin.html' con los datos de productos y categorías
    return render_template('admin.html', productos=productos, categorias=categorias, nombre_usuario=session['nombre_usuario'])

# Ruta alternativa para el panel de administración con diferente rol de usuario
@app.route('/admin2')
def admin2():
    return render_template('admin2.html')

# Ruta para el login
# hacer funcion de logueo paso 6
@app.route('/acceso-login', methods=["GET", "POST"])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        _username = request.form['username']
        _password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE nombre_usuario = %s AND clave = %s', (_username, _password,))
        account = cur.fetchone()

        if account:
            # Almacena información del usuario en la sesión
            session['logueado'] = True
            session['id_usuario'] = account['id_usuario']
            session['id_rol'] = account['id_rol']
            session['nombre_usuario'] = account['nombre_usuario']  # Guardar el nombre de usuario en la sesión
            
            # Redirige a diferentes paneles de administración según el rol del usuario
            if session['id_rol'] == 1:
                return redirect(url_for('admin'))
            elif session['id_rol'] == 2:
                return redirect(url_for('admin2'))
        else:
            # Muestra un mensaje de error si el usuario o la contraseña son incorrectos
            return render_template('index.html', mensaje="Usuario o contraseña incorrectas")
    return render_template('index.html')

#----------------Funciones Crud ---------------------------------#

# Ruta para agregar un producto
@app.route('/add_product', methods=['POST'])
def add_product():
    # Obtiene los datos del formulario
    nombre = request.form['nombre_producto']
    categoria = request.form['categoria_producto']
    descripcion = request.form['descripcion_producto']
    precio = request.form['precio']

    # Inserta un nuevo producto en la base de datos
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO productos (nombre_producto, categoria_producto, descripcion_producto, precio) VALUES (%s, %s, %s, %s)", 
                (nombre, categoria, descripcion, precio))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('admin'))  # Redirige al panel de administración

# Ruta para editar un producto
@app.route('/edit_product/<int:id>', methods=['POST'])
def edit_product(id):
    data = request.get_json()  # Obtiene los datos en formato JSON del cuerpo de la solicitud
    nombre = data['nombre_producto']
    categoria = data['categoria_producto']
    descripcion = data['descripcion_producto']
    precio = data['precio']

    # Actualiza el producto en la base de datos
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE productos 
        SET nombre_producto=%s, categoria_producto=%s, descripcion_producto=%s, precio=%s 
        WHERE id_producto=%s
        """, (nombre, categoria, descripcion, precio, id))
    mysql.connection.commit()
    cur.close()
    return jsonify(success=True)  # Devuelve una respuesta en formato JSON indicando éxito

# Ruta para eliminar un producto
@app.route('/delete_product/<int:id>', methods=['GET'])
def delete_product(id):
    # Elimina el producto de la base de datos
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM productos WHERE id_producto=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('admin'))  # Redirige al panel de administración

# Inicializa la aplicación
""" Esto es para que corra el programa : """
if __name__ == '__main__':
   app.secret_key = "llaveSecreta"  # Llave secreta para la gestión de sesiones
   app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)  # Configuración del servidor

# Explicación de 'pinchellave':
# 'app.secret_key' se usa para firmar cookies de sesión y otras funciones de seguridad en Flask.
# Es importante tener una clave secreta compleja y aleatoria para evitar ataques como la falsificación de cookies.
