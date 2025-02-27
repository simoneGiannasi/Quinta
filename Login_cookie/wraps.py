from functools import wraps

def funzione_decoratore(funzione_parametro):
    @wraps(funzione_parametro)
    def wrapper(*args, **kwargs):
        print("Funzione decorata")
        return funzione_parametro(*args, **kwargs).upper()
    return wrapper


@funzione_decoratore
def echo(message):
    return message

print(echo("ciao"))  # OUTPUT: FUNZIONE DECORATA, CIAO


# Con l'alphabot posso fare una funzione decoratore che uso per i log in cui salvo la funzione che viene eseguita e l'orario in cui viene eseguita