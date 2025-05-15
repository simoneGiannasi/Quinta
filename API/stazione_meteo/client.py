import requests
import datetime



def post():
    n_st = input("Inserisci il nome della stazione: ")
    n_gr = input("Inserisci il nome della grandezza: ")
    data = datetime.datetime.now().isoformat()
    valore = float(input("Inserisci valore: "))
    
    req1 = requests.get("http://localhost:5000/meteo/convGrand/"+str(n_gr))
    req2 = requests.get("http://localhost:5000/meteo/convStaz/"+str(n_st))

    if req1.status_code == 200 and req2.status_code == 200:
        id_gr = req1.json()['id']
        id_st = req2.json()['id']
        
        payload = {
            'id_st': id_st,
            'id_gr': id_gr,
            'data': data,
            'valore': valore
        }

        response = requests.post("http://localhost:5000/meteo/inserimento", json=payload)
        
        if response.status_code == 201:
            print("Dati inseriti con successo.")
        else:
            print("Errore nell'inserimento dei dati.")
            print("Status code:", response.status_code)
    else:
        print("Errore nella richiesta di conversione. Controlla i nomi della stazione e della grandezza.")
        print("Status code stazione:", req2.status_code)
        print("Status code grandezza:", req1.status_code)

def get():
    n_st = input("Inserisci il nome della stazione: ")
    n_gr = input("Inserisci il nome della grandezza: ")

    req1 = requests.get("http://localhost:5000/meteo/convGrand/"+str(n_gr))
    req2 = requests.get("http://localhost:5000/meteo/convStaz/"+str(n_st))

    if req1.status_code == 200 and req2.status_code == 200:
        id_gr = req1.json()['id']
        id_st = req2.json()['id']

        response = requests.get(f"http://localhost:5000/meteo/valMedio?id_st={id_st}&id_gr={id_gr}")

        if response.status_code == 200:
            print("Media:", response.json()['media'])
            print("Massimo:", response.json()['massimo'])
            print("Minimo:", response.json()['min'])
        else:
            print("Errore nella richiesta. Controlla gli ID della stazione e della grandezza.")
            print("Status code:", response.status_code)
    else:
        print("Errore nella richiesta di conversione. Controlla i nomi della stazione e della grandezza.")
        print("Status code stazione:", req2.status_code)
        print("Status code grandezza:", req1.status_code)

if __name__ == "__main__":
    ris = int(input('''Inserisci:
    1: aggiungi misurazione
    2: controlla dati misurazioni    '''))
    if ris == 1:
        post()
    elif ris == 2:
        get()
    else:
        print("Scelta non valida.")
