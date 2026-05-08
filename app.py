from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit

# 1. Configuramos la aplicación
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Piso9' # Una clave para seguridad interna
socketio = SocketIO(app)

# 2. Ruta para el Panel de Control (donde tú escribes)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'Piso9':  # <--- ¡CAMBIA ESTA CONTRASEÑA!
            session['autenticado'] = True
            return redirect(url_for('admin'))
        else:
            return "Contraseña incorrecta", 403
            
    if not session.get('autenticado'):
        return '''
            <form method="post" style="text-align:center; margin-top:100px; font-family:sans-serif;">
                <h2>Acceso Restringido</h2>
                <input type="password" name="password" placeholder="Contraseña">
                <button type="submit">Entrar</button>
            </form>
        '''
    return render_template('admin.html')

# 3. Ruta para la Pantalla de la Sala (donde el paciente ve)
@app.route('/pantalla')
def pantalla():
    return render_template('pantalla.html')

# 4. Lógica de comunicación: Recibe datos de admin y los reenvía a pantalla
@socketio.on('nuevo_turno')
def handle_turno(data):
    print(f"Llamando a: {data['nombre']}") # Esto saldrá en tu consola de Python
    # Enviamos el nombre y el turno a todos los que tengan abierta la web
    emit('actualizar_pantalla', data, broadcast=True)

# 5. Arrancar el servidor
if __name__ == '__main__':
    # 'host=0.0.0.0' permite que otros dispositivos en la misma red vean la web
    socketio.run(app, debug=True, host='0.0.0.0')