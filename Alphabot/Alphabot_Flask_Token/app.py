from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import RPi.GPIO as GPIO
from alphaLib import AlphaBot  

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Nick_Jane'  
bot = AlphaBot()  # Crea un'istanza dell'AlphaBot

#Funzione che genera il token con lo username e la data di scadenza
def generate_token(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token scade in 1 giorno
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')


#Funzione che verifica il token e restituisce l'username se valido, altrimenti None
def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['username']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


#Route per la home page, controlla se l'utente è loggato con il token valido
@app.route('/', methods=['GET'])
def home():
    token = request.cookies.get('token')
    username = verify_token(token)
    if not username:
        return redirect(url_for('login'))
    return render_template('home.html', username=username)


#Route per la pagina di login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['e-mail']
        password = request.form['password']
        return validate(username, password)
    return render_template('login.html')

#Funzione che controlla username e password dal db 
def validate(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    psw = c.execute('SELECT psw FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    
    if psw and check_password_hash(psw[0], password):
        token = generate_token(username)
        response = make_response(redirect(url_for('home')))
        response.set_cookie('token', token, max_age=60*60*24, httponly=True)
        return response
    else:
        alert = "Credenziali non valide!"
        return render_template('login.html', alert=alert)


# Route per la pagina di creazione di un account
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['e-mail']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        # Controlla se l'utente esiste già
        existing_user = c.execute('SELECT username FROM users WHERE username = ?', (username,)).fetchone()
        if existing_user:
            conn.close()
            return render_template('create_account.html', alert="Utente già esistente!")
        
        c.execute('INSERT INTO users (username, psw) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    
    return render_template('create_account.html')


# Route per la pagina di logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('token')
    return response

#Nuova rotta per gestire i comandi dell'AlphaBot
@app.route('/comando', methods=['POST'])
def comando():
    # Verifica l'autenticazione
    token = request.cookies.get('token')
    username = verify_token(token)
    if not username:
        return jsonify({'status': 'Non autorizzato'}), 401
    
    try:
        # Imposta il modo GPIO qui per assicurarsi che sia correttamente configurato prima di ogni comando
        try:
            GPIO.setmode(GPIO.BCM)
        except RuntimeError:
            # Se il modo è già impostato, possiamo continuare
            pass
        
        data = request.get_json()
        action = data.get('action')
        
        if action == 'avanti':
            bot.forward()
            response = {'status': 'Il robot si muove in avanti'}
        elif action == 'indietro':
            bot.backward()
            response = {'status': 'Il robot si muove indietro'}
        elif action == 'sinistra':
            bot.left()
            response = {'status': 'Il robot gira a sinistra'}
        elif action == 'destra':
            bot.right()
            response = {'status': 'Il robot gira a destra'}
        elif action == 'stop':
            bot.stop()
            response = {'status': 'Il robot si è fermato'}
        else:
            return jsonify({'status': 'Comando non riconosciuto'}), 400
            
        return jsonify(response)
    except Exception as e:
        return jsonify({'status': f'Errore: {str(e)}'}), 500


def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    password = generate_password_hash("simo")
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        psw TEXT NOT NULL
    );
    INSERT INTO users (username, psw) VALUES (simone.giannasi@itiscuneo.eu, ?)''', (password,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    try:
        init_db()
        app.run(debug=True, host='0.0.0.0', port=4444)
    finally:
        GPIO.cleanup()  # Only clean up when the app completely exits