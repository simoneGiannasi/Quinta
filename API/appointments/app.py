import sqlite3
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import datetime

app = Flask(__name__)
api = Api(app)



class Prenotazioni(Resource):
# GET /appointments/<id>: restituisce i dettagli dell’appuntamento con l’ID specificato.
# GET /appointments: restituisce la lista di tutti gli appuntamenti.
    def get(self, id=None):
        conn = sqlite3.connect('./prenotazioni.db')
        cursor = conn.cursor()
        if id is None:
            cursor.execute("SELECT * FROM prenotazione")
            rows = cursor.fetchall()
            result = []
            for row in rows:
                result.append({
                    'id': row[0],
                    'nome': row[1],
                    'cognome': row[2],
                    'dataN': row[3],
                    'ora': row[4],
                    'durata': row[5],
                    'motivo': row[6]
                })
            conn.close()
            return jsonify(result)
        else:
            cursor.execute("SELECT * FROM prenotazione WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row is None:
                return {'message': 'Appuntamento non trovato'}, 404
            result = {
                'id': row[0],
                'nome': row[1],
                'cognome': row[2],
                'dataN': row[3],
                'ora': row[4],
                'durata': row[5],
                'motivo': row[6]
            }
            conn.close()
            return jsonify(result)

# POST /appointments: aggiunge un nuovo appuntamento. Il client invia un oggetto JSON con i dati richiesti (escluso l’ID, che viene generato automaticamente).
# Quando si aggiunge o modifica un appuntamento (POST o PUT), il sistema deve impedire la sovrapposizione: non possono esserci due appuntamenti nella stessa data e allo stesso orario.
# In caso di conflitto, il server restituisce un errore 409 Conflict con un messaggio esplicativo.

    def post(self):
        conn = sqlite3.connect('./prenotazioni.db')
        cursor = conn.cursor()
        data = request.get_json()
        nome = data['nome']
        cognome = data['cognome']
        dataN = data['dataN']
        ora = data['ora']
        motivo = data['motivo']
        durata = data['durata']

        if dataN is None or ora is None or durata is None or motivo is None:
            return {'message': 'Dati non validi'}, 400
        

        # Verifica se l'appuntamento esiste già
        cursor.execute("SELECT ora, durata FROM prenotazione WHERE dataN = ?", (dataN,))
        appuntamenti_stessa_data = cursor.fetchall()
    
        if appuntamenti_stessa_data is not None:
            for appuntamento in appuntamenti_stessa_data:
                if appuntamento[0] >= ora and appuntamento[0] < (datetime.datetime.strptime(ora, '%H:%M') + datetime.timedelta(minutes=durata)).strftime('%H:%M'):
                    # Se l'orario dell'appuntamento esistente è compreso nell'intervallo dell'appuntamento da aggiungere
                    conn.close()
                    return {'message': 'CONFLICT: Appuntamento già presente per questo giorno e questo orario'}, 409
                if (datetime.datetime.strptime(ora, '%H:%M') + datetime.timedelta(minutes=durata)) >= appuntamento[0] and ora < (datetime.datetime.strptime(appuntamento[0], '%H:%M') + datetime.timedelta(minutes=appuntamento[1])).strftime('%H:%M'):
                    # Se l'orario dell'appuntamento da aggiungere è compreso nell'intervallo dell'appuntamento esistente
                    conn.close()
                    return {'message': 'CONFLICT: Appuntamento già presente per questo giorno e questo orario'}, 409
        
                
        cursor.execute("INSERT INTO prenotazione (nome, cognome, dataN, ora, durata, motivo) VALUES (?, ?, ?, ?, ?, ?)",
                        (nome, cognome, dataN, ora,durata, motivo))
        conn.commit()
        id = cursor.lastrowid
        conn.close()
        return {'id': id, 'message': 'Appuntamento creato con successo'}, 201
    

    # PUT /appointments/<id>: modifica un appuntamento esistente.
    def put(self, id):
        nome = request.json.get('nome', None)
        cognome = request.json.get('cognome', None)
        data = request.get_json()
        dataN = data.get('dataN', None)
        ora = data.get('ora', None)
        durata = data.get('durata', None)
        motivo = data.get('motivo', None)
        


        conn = sqlite3.connect('./prenotazioni.db')
        cursor = conn.cursor()


        if (dataN is None and ora is None and durata is None and motivo is None) or (dataN is not None and ora is None and durata is not None) or (ora is not None and dataN is None and durata is not None):
            return {'message': 'Dati non validi'}, 400
        

        # Verifica se l'appuntamento esiste già
        if dataN is not None and ora is not None and durata is not None:
            cursor.execute("SELECT ora, durata FROM prenotazione WHERE dataN = ? AND id != ?", (dataN,id,))
            appuntamenti_stessa_data = cursor.fetchall()
            
            if appuntamenti_stessa_data is not None:
                for appuntamento in appuntamenti_stessa_data:
                    if appuntamento[0] >= ora and appuntamento[0] < (datetime.datetime.strptime(ora, '%H:%M') + datetime.timedelta(minutes=durata)).strftime('%H:%M'):
                        # Se l'orario dell'appuntamento esistente è compreso nell'intervallo dell'appuntamento da aggiungere
                        conn.close()
                        return {'message': 'CONFLICT: Appuntamento già presente per questo giorno e questo orario'}, 409
                    if (datetime.datetime.strptime(ora, '%H:%M') + datetime.timedelta(minutes=durata)) >= appuntamento[0] and ora < (datetime.datetime.strptime(appuntamento[0], '%H:%M') + datetime.timedelta(minutes=appuntamento[1])).strftime('%H:%M'):
                        # Se l'orario dell'appuntamento da aggiungere è compreso nell'intervallo dell'appuntamento esistente
                        conn.close()
                        return {'message': 'CONFLICT: Appuntamento già presente per questo giorno e questo orario'}, 409

        # Aggiorna solo i campi forniti
        query = "UPDATE prenotazione SET "
        params = []
        if nome is not None:
            query += "nome = ?, "
            params.append(nome)
        if cognome is not None:
            query += "cognome = ?, "
            params.append(cognome)
        if dataN is not None:
            query += "dataN = ?, "
            params.append(dataN)
        if ora is not None:
            query += "ora = ?, "
            params.append(ora)
        if durata is not None:
            query += "durata = ?, "
            params.append(durata)
        if motivo is not None:
            query += "motivo = ?, "
            params.append(motivo)
        query = query.rstrip(", ") + " WHERE id = ?"
        params.append(id)
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return {'message': 'Appuntamento aggiornato con successo'}, 200
        
        
    # DELETE /appointments/<id>: elimina l’appuntamento con l’ID specificato
    def delete(self, id):
        conn = sqlite3.connect('./prenotazioni.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM prenotazione WHERE id = ?", (id,))
        if(conn.commit()) == 0:
            conn.close()
            return {'message': 'Appuntamento non trovato'}, 404
        conn.close()
        return {'message': 'Appuntamento eliminato con successo'}, 200


api.add_resource(Prenotazioni, "/appointments/<int:id>", "/appointments")


def crea_db():
    conn = sqlite3.connect('./prenotazioni.db')
    cursor = conn.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS prenotazione (  
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cognome TEXT NOT NULL,
                    dataN TEXT NOT NULL,
                    ora TEXT NOT NULL,
                    durata INTEGER NOT NULL CHECK (durata > 0),
                    motivo TEXT NOT NULL);
                   ''')
    # cursor.execute('''
    #                INSERT INTO prenotazione (nome, cognome, dataN, ora, durata, motivo) VALUES
    #                ('Mario', 'Rossi', '2023-10-01', '10:00', 30, 'Controllo'),
    #                ('Luigi', 'Verdi', '2023-10-02', '11:00', 60, 'Visita'),
    #                ('Anna', 'Bianchi', '2023-10-03', '12:00', 45, 'Esame')''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    crea_db()
    app.run(debug=True)
    