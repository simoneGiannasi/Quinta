import sqlite3
import jwt
from datetime import datetime, timedelta
from flask import Flask, render_template, request

app = Flask(__name__)
app.config["SECRET_KEY"] = "SimoneGiannasi"


def crea_token(url, data_scadenza):
    #Funzione che crea il token, si connette al db e inserisce i dati del token nel db, infine chiude la connessione con il db e restiìtuisce il token
    payload = {
        "url": url,
        "exp": datetime.utcnow() + timedelta(minutes=int(data_scadenza))
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    conn = sqlite3.connect("links.db")
    c = conn.cursor()
    c.execute('''INSERT INTO links(token, url, valido)
              VALUES
              (?,?,1)
              ''', (token, url))
    conn.commit()
    conn.close()
    return token


    

    
@app.route("/", methods=["GET", "POST"])
def genero_link():
    if request.method == "POST":
        url = request.form["url"]
        data_scadenza = request.form["expiration"]
        token = crea_token(url, data_scadenza)
        link = "http://127.0.0.1:5678/shared/"+token
        return render_template("index_V.html", link = link)
    return render_template("index_V.html")


@app.route("/shared/<token>", methods=["GET"])
def pagina_link(token):
    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')

    conn = sqlite3.connect("links.db")
    c = conn.cursor()
    dati_db = c.execute("SELECT * FROM links WHERE token==?", (token,)).fetchone()
    conn.commit()
    conn.close()

    if not dati_db:
        return render_template("shared_V.html", message="Token non valido")
    if int(dati_db[3]) == 0:
        return render_template("shared_V.html", message = "Token non più valido")
    
    # Altrimenti è corretto, quindi l'ho gia usato e lo metto a 0
    conn = sqlite3.connect("links.db")
    c = conn.cursor()
    c.execute('''UPDATE links 
                SET valido = 0
                WHERE token == ?
              ''', (token,))
    conn.commit()
    conn.close()
    url = payload["url"]
    return render_template("shared_V.html", url = "http://"+url)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5678)




# Risposta alla domanda:
# I token vengono spesso usati in siti single-page perchè andrebbero passati da una pagina all'altra ma questo provoca probliemi di sicurezza perchpè nel body non è sicuro, nell'url nemmeno quindi vengono spesso messi dentro i cookie per essere passati tra le pagine.
# cookie si salvono anche sul server, i token solo sul client. Per sapere che il token sia mio uso una chiave segrteta per criptare e decriptare il token. 
# In questo modo, se qualcuno riesce a rubare il token, non potrà utilizzarlo perché non conosce la chiave di decriptazione.
# I token sono in chiaro, non sono criptati, quindi se qualcuno si impossessa del token di qualcuno quando è ancora valido, questo potrò fare l'accesso come la
# persona a cui il token è assegnato.
