import sqlite3

def main():
    conn = sqlite3.connect('users.db')  # Crea un file SQLite chiamato 'users.db'
    curs = conn.cursor()
    curs.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nome TEXT NOT NULL,
                 cognome TEXT NOT NULL,
                 eta INTEGER NOT NULL)''')
    curs.execute("INSERT INTO users(nome, cognome, eta) VALUES ('simone', 'giannasi', 18), ('nico','dutto',19)")
    conn.commit()

if __name__ == "__main__":
    main()