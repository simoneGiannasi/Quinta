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

@app.route('/login', methods=['GET','POST'])
def login():
  if request.method == 'POST':
    username = request.form['e-mail']
    password = request.form['password']
    return validate(username,password)

  return render_template('login.html')

def validate(username,password):
  # Connetti al database e cerca l'utente
  conn = sqlite3.connect('users.db')
  c = conn.cursor()
  c.execute('SELECT psw FROM users WHERE username = ?', (username,))
  stored_password = c.fetchone() # restituisce la PRIMA riga
  if stored_password and check_password_hash(stored_password[0], password):
      # Login riuscito
      response =make_response(redirect(url_for('home')))  # make_response serve a creare una risposta HTTP personalizzata (aggiungiendo i cookie)
      response.set_cookie('username',username,max_age=60*60*24) # Il cookie dura 1 giorno
      return response
  else:
      # Login fallito
      return render_template('login.html', alert="Invalid credential!")


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['e-mail']
        password = request.form['password']

        # Cripta la password prima di salvarla
        hashed_password = generate_password_hash(password,method='pbkdf2:sha256')
        
        # Salva l'utente nel database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()



        return redirect(url_for('login'))  # Dopo aver aggiunto l'utente, ritorna alla pagina principale
    
    return render_template('create_account.html')

@app.route('/logout')
def logout():
   response = make_response(redirect(url_for('login')))
   response.delete_cookie('username')
   return response

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0',port=4444)