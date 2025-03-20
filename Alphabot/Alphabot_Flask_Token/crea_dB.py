import sqlite3
from werkzeug.security import generate_password_hash

def main():
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

if __name__ == "__main__":
    main()