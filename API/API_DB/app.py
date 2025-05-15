from flask import Flask, jsonify, request
import sqlite3
import requests # Per fare richieste CURL
import sqlite3

app = Flask(__name__)
db_name = "users.db"




# # CREATE - Aggiungi un nuovo studente
@app.route("/studenti", methods=["POST"])
def create_studente():
    try:
        # estrae il corpo della richiesta HTTP in formato JSON e lo converte in un dizionario Python
        dati = request.json
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (nome, cognome, eta) VALUES (?, ?, ?)", (dati["nome"], dati["cognome"], dati["eta"]))
        conn.commit()
        return jsonify({"messaggio": "Studente aggiunto"}), 201
    except:
        return jsonify({"errore": "Impossibile aggiungere lo studente"}), 500



# READ - Ottieni tutti gli studenti
@app.route("/studenti", methods=["GET"])
def get_studenti():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    studenti = cursor.fetchall()
    conn.close()
    return jsonify(studenti)

# READ - Ottieni un singolo studente per ID
@app.route("/studenti/<int:id>", methods=["GET"])
def get_studente(id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
    studente = cursor.fetchone()
    conn.close()
    if studente:
        return jsonify(studente)
    return jsonify({"errore": "Studente non trovato"}), 404
    

# # UPDATE - Modifica i dati di uno studente
@app.route("/studenti/<int:id>", methods=["PUT"])
def update_studente(id):
    # try: 
    #     dati = request.json
    #     conn = sqlite3.connect(db_name)
    #     cursor = conn.cursor()
    #     cursor.execute("UPDATE users SET nome=?, cognome=?, eta=? WHERE id=?", (dati["nome"], dati["cognome"], dati["eta"], id))
    #     conn.commit()
    #     conn.close()
    #     return jsonify({"messaggio": "Studente modificato"})
    # except:
    #     return jsonify({"errore": "Studente non trovato"}), 404
    
    dati = request.json
    if not dati:
        return jsonify({"errore": "Nessun dato da modificare"}), 400
    campi_validi = ["nome", "cognome", "eta"]
    query_parts = [f"{campo} = ?" for campo in campi_validi if campo in dati]
    valori = [dati[campo] for campo in campi_validi if campo in dati]
    if not query_parts:
        return jsonify({"errore": "Nessun dato da modificare"}), 400
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        query = f"UPDATE users SET {', '.join(query_parts)} WHERE id = ?"
        valori.append(id)
        cursor.execute(query, valori)
        conn.commit()
        conn.execute("SELECT * FROM users WHERE id = ?", (id,))
        studente = cursor.fetchone()
        return jsonify(studente) if studente else jsonify({"errore": "Studente non trovato"}), 404


# DELETE - Elimina uno studente
@app.route("/studenti/<int:id>", methods=["DELETE"])
def delete_studente(id):
    try: 
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return jsonify({"messaggio": "Studente eliminato"})
    except:
        return jsonify({"errore": "Studente non trovato"}), 404



if __name__ == "__main__":
    app.run(debug=True)

