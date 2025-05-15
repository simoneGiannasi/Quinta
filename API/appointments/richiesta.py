import requests

def post():
    try:
        nome = input("Inserisci nome: ")
        cognome = input("Inserisci cognome: ")
        data_appuntamento = input("Inserisci la data dell'appuntamento (YYYY-MM-DD): ")
        ora = input("Inserisci ora (HH:MM): ")
        motivo = input("Inserisci motivo: ")
        durata = input("Inserisci durata (in minuti): ")
        
        
        url = "http://127.0.0.1:5000/appointments"  # Endpoint dell'API
        dati_studente = {
            "nome": nome,
            "cognome": cognome,
            "dataN": data_appuntamento,
            "ora": ora,
            "motivo": motivo,
            "durata": durata
        }

        # Invia la richiesta POST con i dati JSON
        response = requests.post(url, json=dati_studente)

        # Verifica la risposta del server
        if response.status_code == 201:
            print("Appntamento aggiunto con successo!")
            print(response.json())  # Mostra il messaggio di conferma e i dettagli dello studente
        else:
            print(f"Errore: {response.status_code}")
            print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Errore nella richiesta HTTP: {e}")


# def put():
#     try:
#         id = int(input("Inserisci l'ID dello studente da modificare: "))
#         nome = input("Inserisci nuovo nome: ")
#         cognome = input("Inserisci nuovo cognome: ")
        
#         # Input validation for age
#         while True:
#             try:
#                 eta = int(input("Inserisci nuova eta: "))
#                 if eta <= 0:
#                     print("L'età deve essere un numero positivo.")
#                     continue
#                 break
#             except ValueError:
#                 print("Per favore, inserisci un numero valido per l'età.")
        

#         url = "http://127.0.0.1:5000/studenti/"+str(id)  # Endpoint dell'API
#         dati_studente = {
#             "nome": nome,
#             "cognome": cognome,
#             "eta": eta
#         }

#         # Invia la richiesta PUT con i dati JSON
#         response = requests.put(url, json=dati_studente)

#         # Verifica la risposta del server
#         if response.status_code == 200:
#             print("Studente aggiornato con successo!")
#             print(response.json())  # Mostra il messaggio di conferma e i dettagli dello studente
#         else:
#             print(f"Errore: {response.status_code}")
#             print(response.json())
#     except requests.exceptions.RequestException as e:
#         print(f"Errore nella richiesta HTTP: {e}")


def delete():
    try:
        id = int(input("Inserisci l'ID dello studente da eliminare: "))
        url = "http://127.0.0.1:5000/appointments/"+str(id)
        # Invia la richiesta DELETE
        response = requests.delete(url)
        # Verifica la risposta del server
        if response.status_code == 200:
            print("Studente eliminato con successo!")
        else:
            print(f"Errore: {response.status_code}")
            print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Errore nella richiesta HTTP: {e}")




if __name__ == "__main__":
    ris = input('''Inserisci:
    1: aggiungi appuntamento
    2: modifica appuntamento
    3: elimina appuntamento    ''')
    if ris == "1":
        post()
    # elif ris == "2":
    #     put()
    elif ris == "3":
        delete()
    else:
        print("Scelta non valida.")
