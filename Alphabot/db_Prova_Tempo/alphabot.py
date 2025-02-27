import socket
#import alphaLib
import sqlite3
import time

# Impostazione dell'indirizzo del server
alphabot_address = ("localhost", 12345)
DB_NAME = "./db_Prova_Tempo/movimenti.db"


def main():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    dati = cursor.execute('''SELECT * FROM movimento''').fetchall()
    
    movimenti_speciali_dict = {}
    for com in dati:
        movimenti_speciali_dict[com[0]] = com[1]
    print(movimenti_speciali_dict)

    comandi_speciali_iop = False

    # Creazione del socket TCP del server
    alphabot_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    alphabot_tcp.bind(alphabot_address)
    alphabot_tcp.listen(1)
    print("Server AlphaBot in ascolto...")
    #alpha = alphaLib.AlphaBot()
    
    try:
        #alpha.setMotor(0, 0)
        while True:
            client, address = alphabot_tcp.accept()
            print(f"Connessione accettata da {address}")
            while True:
                messaggio = client.recv(4096).decode('utf-8')
                if messaggio:
                    if messaggio == 'end':
                        print("Chiusura connessione...")
                        client.close()
                        break
                    comandi = messaggio.split(",")  # Splitta i comandi
                    if len(comandi) == 2 and comandi_speciali_iop==False:
                        left = comandi[0]
                        right = comandi[1]
                        print(f"Comando ricevuto: {left},{right}")
                        #alpha.setMotor(left, right)
                    else:
                        comando = comandi[0]
                        comandi_speciali_iop = True
                        gestisciComandiSpeciali(comando, movimenti_speciali_dict)
                        comandi_speciali_iop = False
                        
                else:
                    break  # Chiude la connessione se non ci sono più messaggi
    finally:
        alphabot_tcp.close()

def gestisciComandiSpeciali(comando, movimenti_speciali_dict):
    if comando in movimenti_speciali_dict:
        print(movimenti_speciali_dict[comando])
        movimento = movimenti_speciali_dict[comando]
        gestioneMovimento(movimento)


def gestioneMovimento(movimento):
    pezzi_movimento = movimento.split(',')

    for pezzo_movimento in pezzi_movimento:
        pezzo = pezzo_movimento.split(':')
        wasd = pezzo[0] # dice wasd in base a dove andare
        tempo = int(pezzo[1]) # dice il tempo per cui deve andare
        print(f"Wasd={wasd},tempo={tempo}")
        
        # Registra il tempo di inizio
        start_time = time.time()
        # Continua ad eseguire finché non sono trascorsi n secondi
        while time.time() - start_time < tempo:
            if wasd == "w":
                #alpha.setMotor(-50, 50)
                pass
            if wasd == "s":
                #alpha.setMotor(50, -50)
                pass
            if wasd == "a":
                #alpha.setMotor(0, 30)
                pass
            if wasd == "d":
                #alpha.setMotor(-30, 0)
                pass
        

if __name__ == '__main__':
    main()