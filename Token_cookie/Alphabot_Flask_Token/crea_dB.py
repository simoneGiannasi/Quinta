import sqlite3

def main():
    conn = sqlite3.connect('users.db')  # Crea un file SQLite chiamato 'users.db'
    curs = conn.cursor()
    curs.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL,
                 psw TEXT NOT NULL)''')
    #curs.execute("DELETE FROM users WHERE username = 'simone.giannasi@itiscuneo.eu'")
    conn.commit()

if __name__ == "__main__":
    main()