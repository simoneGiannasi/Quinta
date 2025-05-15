import sqlite3
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import datetime

NOME_DB = 'meteo_db.db'

app = Flask(__name__)
api = Api(app)




class conversione_grandezza(Resource):
    def get(self, nome):
        conn = sqlite3.connect(NOME_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT id_misura FROM grandezze WHERE grandezza_misurata LIKE ?", (nome,))
        id_misura = cursor.fetchone()
        conn.close()
        if id_misura:
            return jsonify({'id': id_misura[0]})
        else:
            return {'message': "id sbagliato"}, 404

class conversione_stazione(Resource):
    def get(self, nome):
        conn = sqlite3.connect(NOME_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT id_stazione FROM stazioni WHERE nome LIKE ?", (nome,))
        id_stazione = cursor.fetchone()
        conn.close()
        if id_stazione:
            return jsonify({'id': id_stazione[0]})
        else:
            return {'message': "id sbagliato"}, 404

class inserimento_dati(Resource):
    def post(self):
        id_st = request.json['id_st']
        id_gr = request.json['id_gr']
        data = request.json['data']
        valore = request.json['valore']
        if id_st and id_gr and data and valore:
            conn = sqlite3.connect(NOME_DB)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO misurazioni (id_stazione, id_grandezza, data_ora,
                           valore) VALUES (?, ?, ?, ?)''', (id_st, id_gr, data, valore))
            conn.commit()
            conn.close()
            return {'message': 'Dati inseriti con successo'}, 201
        else:
            return {'message': 'Dati non validi'}, 400

class valori_medi(Resource):
    def get(self):
        id_st = request.args.get('id_st')
        id_gr = request.args.get('id_gr')
        
        if id_st and id_gr:
            conn = sqlite3.connect(NOME_DB)
            cursor = conn.cursor()  
            cursor.execute('''SELECT AVG(valore) as avg, MAX(valore) as max, MIN(valore) as min
                           FROM misurazioni 
                           WHERE id_stazione = ? 
                           AND id_grandezza = ?''', (id_st, id_gr))
            dati = cursor.fetchone()
            conn.close()
            if dati:
                return jsonify({'media': dati[0], 'massimo': dati[1], 'min': dati[2]})
        else:
            return {'error': "id sbagliati"}, 404

api.add_resource(conversione_stazione, '/meteo/convStaz/<string:nome>')
api.add_resource(conversione_grandezza, '/meteo/convGrand/<string:nome>')
api.add_resource(inserimento_dati, '/meteo/inserimento')
api.add_resource(valori_medi, '/meteo/valMedio')

if __name__ == '__main__':
    app.run(debug=True)
