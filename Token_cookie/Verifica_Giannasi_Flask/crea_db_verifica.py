import sqlite3

conn = sqlite3.connect("links.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS links (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    token TEXT NOT NULL,
                    url TEXT NOT NULL,
                    valido INTEGER NOT NULL
                )''')
conn.commit()
conn.close()