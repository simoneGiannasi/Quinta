from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a random secret key

def generate_token(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token expires in 1 day
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['username']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/', methods=['GET'])
def home():
    token = request.cookies.get('token')
    username = verify_token(token)
    if not username:
        return redirect(url_for('login'))
    return render_template('home.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['e-mail']
        password = request.form['password']
        return validate(username, password)
    return render_template('login.html')

def validate(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    psw = c.execute('SELECT psw FROM users WHERE username = ?', (username,)).fetchone()
    if psw:
        print(f"Stored hashed password: {psw[0]}")
    if psw and check_password_hash(psw[0], password):
        token = generate_token(username)
        response = make_response(redirect(url_for('home')))
        response.set_cookie('token', token, max_age=60*60*24)
        return response
    else:
        alert = "Invalid credential!"
        return render_template('login.html', alert=alert)

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['e-mail']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        print(f"Hashed password: {hashed_password}")

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, psw) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    
    return render_template('create_account.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('token')
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4444)