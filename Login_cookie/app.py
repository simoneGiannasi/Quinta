from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)



@app.route('/', methods=['GET'])
def home():
    username = request.cookies.get('username') # legge il cookie "username"
    if not username:
       return redirect(url_for('login')) # se non c'è il cookie, ritorna al login
    return render_template('home.html', username=username)  

# Funzione per il login
@app.route('/login', methods=['GET','POST'])
def login():
    # Se il metodo è post allora prendo dal form lo username e la password
    if request.method == 'POST':
        username = request.form['e-mail']
        password = request.form['password']
        return validate(username,password) # Valido username e password per capire se l'account esiste
    return render_template('login.html')

def validate(username,password):
    # Connetti al database e cerca l'utente
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    psw = c.execute('SELECT psw FROM users WHERE username = ?', (username,)).fetchall()
    print(psw[0][0])
    print(password)
    if psw[0][0] == password:
        print("Login Riuscito")
        response =make_response(redirect(url_for('home')))  # make_response serve a creare una risposta HTTP personalizzata (aggiungiendo i cookie)
        response.set_cookie('username',username,max_age=60*60*24) # Il cookie dura 1 giorno
        return response
    else:
        print("Login Fallito")
        alert =  "Invalid credential!"
        return render_template('login.html', alert=alert)



@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['e-mail']
        password = request.form['password']

        # Salvo l'utente nel database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, psw) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))  # Dopo aver aggiunto l'utente, ritorna alla pagina principale
    
    return render_template('create_account.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('username')
    return response

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0',port=4444)