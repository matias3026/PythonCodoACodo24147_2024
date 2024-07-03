#paso 1
from flask import Flask
from flask import render_template, redirect, request, Response , session , url_for, jsonify
from flask_mysqldb import MySQL, MySQLdb


#paso 2
app = Flask(__name__,template_folder='template', static_folder='static')


#paso 3
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cafeteria'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app) #esto inicializa mysql

#paso 4 redigir a ruta del index
@app.route('/')
def home():
    return render_template('index.html')   #login

#paso 5 redigir a ruta del admin--la ruta comentada era antes de funcion mostrar productos
# @app.route('/admin')
# def admin():
#     return render_template('admin.html')

@app.route('/admin')
def admin():
    if 'nombre_usuario' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    productos = cur.fetchall()

    cur.execute('SELECT DISTINCT categoria_producto FROM productos')
    categorias = [row['categoria_producto'] for row in cur.fetchall()]

    cur.close()
    return render_template('admin.html', productos=productos, categorias=categorias, nombre_usuario=session['nombre_usuario'])
  

@app.route('/admin2')
def admin2():
    return render_template('admin2.html') 


#hacer funcion de logueo paso 6
@app.route('/acceso-login', methods= ["GET", "POST"])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        _username = request.form['username']
        _password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE nombre_usuario = %s AND clave = %s', (_username, _password,))
        account = cur.fetchone()

        if account:
            session['logueado'] = True
            session['id_usuario'] = account['id_usuario']
            session['id_rol'] = account['id_rol']
            session['nombre_usuario'] = account['nombre_usuario']  # Guardar el nombre de usuario en la sesión
            
            if session['id_rol'] == 1:
                return redirect(url_for('admin'))
            elif session['id_rol'] == 2:
                return redirect(url_for('admin2'))
        else:
            return render_template('index.html', mensaje="Usuario o contraseña incorrectas")
    return render_template('index.html')



#----------------Funciones Crud ---------------------------------#

# Ruta para agregar un producto
@app.route('/add_product', methods=['POST'])
def add_product():
    nombre = request.form['nombre_producto']
    categoria = request.form['categoria_producto']
    descripcion = request.form['descripcion_producto']
    precio = request.form['precio']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO productos (nombre_producto, categoria_producto, descripcion_producto, precio) VALUES (%s, %s, %s, %s)", 
                (nombre, categoria, descripcion, precio))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('admin'))

# Ruta para editar un producto
@app.route('/edit_product/<int:id>', methods=['POST'])
def edit_product(id):
    data = request.get_json()
    nombre = data['nombre_producto']
    categoria = data['categoria_producto']
    descripcion = data['descripcion_producto']
    precio = data['precio']

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE productos 
        SET nombre_producto=%s, categoria_producto=%s, descripcion_producto=%s, precio=%s 
        WHERE id_producto=%s
        """, (nombre, categoria, descripcion, precio, id))
    mysql.connection.commit()
    cur.close()
    return jsonify(success=True)

# Ruta para eliminar un producto
@app.route('/delete_product/<int:id>', methods=['GET'])
def delete_product(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM productos WHERE id_producto=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('admin'))












""" Esto es para que 
corra el programa :
"""
# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
   app.secret_key = "pinchellave"
   app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)