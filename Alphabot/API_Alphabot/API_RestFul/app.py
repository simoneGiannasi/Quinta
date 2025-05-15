from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# Dizionario di studenti
studenti = {
    1: {"nome": "Mario", "cognome": "Rossi", "eta": 18},
    2: {"nome": "Luca", "cognome": "Bianchi", "eta": 19},
    3: {"nome": "Giulia", "cognome": "Verdi", "eta": 17}
}

class Studenti(Resource):
    def get(self):
        return studenti
   
    def post(self):
        dati = request.json
       
        nuovo_id = max(studenti.keys(), default=0) + 1
        studenti[nuovo_id] = {
            "nome": dati.get("nome"),
            "cognome": dati.get("cognome"),
            "eta": dati.get("eta")
        }
        return {"messaggio": "Studente aggiunto", "id": nuovo_id, "studente": studenti[nuovo_id]}, 201
   
    def head(self):
        return "", 200
   
    def options(self):
        return {
            "allow": "GET, POST, OPTIONS, HEAD"
        }, 200, {
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS, HEAD",
            "Access-Control-Allow-Origin": "*"
        }

class Studente(Resource):
    def get(self, id):
            studente = studenti.get(id)
            if studente:
                return jsonify(studente)
            return {"errore": "Studente non trovato"}, 404

    def patch(self, id):
        if id in studenti:
            dati = request.json
            studenti[id].update(dati)
            return jsonify({"messaggio": "Studente aggiornato", "studente": studenti[id]})
        return {"errore": "Studente non trovato"}, 404
   
    def put(self, id):
        if id in studenti:
            dati = request.json
            # Controllo campi obbligatori (nome, cognome, eta)
            if not all(k in dati for k in ("nome", "cognome", "eta")):
                return {"errore": "Campi mancanti. Servono: nome, cognome, eta"}, 400

            # Sovrascrive completamente la risorsa esistente
            studenti[id] = {
                "nome": dati["nome"],
                "cognome": dati["cognome"],
                "eta": dati["eta"]
            }
            return {"messaggio": "Studente aggiornato (completo)", "studente": studenti[id]}
        return {"errore": "Studente non trovato"}, 404
           

    def delete(self,id):
        if id in studenti:
            del studenti[id]
            return jsonify({"messaggio": "Studente eliminato"})
        return {"errore": "Studente non trovato"}, 404
   
    def head(self, id):
        if id in studenti:
            return "", 200
        return "", 404

    def options(self, id):
        return {
            "allow": "GET, PUT, PATCH, DELETE, OPTIONS, HEAD"
        }, 200, {
            "Access-Control-Allow-Methods": "GET, PUT, PATCH, DELETE, OPTIONS, HEAD",
            "Access-Control-Allow-Origin": "*"
        }


api.add_resource(Studenti, "/studenti")
api.add_resource(Studente, "/studenti/<int:id>")

if __name__ == "__main__":
   
    app.run(debug=True)
