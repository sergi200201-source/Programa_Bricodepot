from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        if nombre.strip().lower() != 'sergi':
            return redirect(url_for('unauthorized'))
        session['nombre'] = nombre
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/index')
def index():
    if 'nombre' not in session:
        return redirect(url_for('unauthorized'))
    return render_template('index.html', nombre=session['nombre'])

@app.route('/unauthorized')
def unauthorized():
    return render_template('unauthorized.html')

@app.route('/logout')
def logout():
    session.pop('nombre', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)