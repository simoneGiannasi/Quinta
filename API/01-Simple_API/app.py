from flask import Flask, jsonify, request
import sqlite3
import requests # Per fare richieste CURL

app = Flask(__name__)

# Dizionario di studenti
studenti = {
    1: {"nome": "Mario", "cognome": "Rossi", "eta": 18},
    2: {"nome": "Luca", "cognome": "Bianchi", "eta": 19},
    3: {"nome": "Giulia", "cognome": "Verdi", "eta": 17}
}

# CREATE - Aggiungi un nuovo studente
@app.route("/studenti", methods=["POST"])
def create_studente():
    # estrae il corpo della richiesta HTTP in formato JSON e lo converte in un dizionario Python
    dati = request.json
    
    nuovo_id = max(studenti.keys(), default=0) + 1
    studenti[nuovo_id] = {
        "nome": dati.get("nome"),
        "cognome": dati.get("cognome"),
        "eta": dati.get("eta")
    }
    return jsonify({"messaggio": "Studente aggiunto", "id": nuovo_id, "studente": studenti[nuovo_id]}), 201

# READ - Ottieni tutti gli studenti
@app.route("/studenti", methods=["GET"])
def get_studenti():
    return jsonify(studenti)

# READ - Ottieni un singolo studente per ID
@app.route("/studenti/<int:id>", methods=["GET"])
def get_studente(id):
    studente = studenti.get(id)
    if studente:
        return jsonify(studente)
    return jsonify({"errore": "Studente non trovato"}), 404

# UPDATE - Modifica i dati di uno studente
@app.route("/studenti/<int:id>", methods=["PUT"])
def update_studente(id):
    if id in studenti:
        dati = request.json
        studenti[id].update(dati)
        return jsonify({"messaggio": "Studente aggiornato", "studente": studenti[id]})
    return jsonify({"errore": "Studente non trovato"}), 404

# DELETE - Elimina uno studente
@app.route("/studenti/<int:id>", methods=["DELETE"])
def delete_studente(id):
    if id in studenti:
        del studenti[id]
        return jsonify({"messaggio": "Studente eliminato"})
    return jsonify({"errore": "Studente non trovato"}), 404



if __name__ == "__main__":
    
    app.run(debug=True)

