from flask import Flask, render_template, request as request_flask, redirect, url_for, make_response
from flask_dance.contrib.github import make_github_blueprint
from dotenv import load_dotenv
import os
import requests

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")



github_bp = make_github_blueprint(
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    scope=["user:email"]
    redirect_url="/auth/callback"
)
app.register_blueprint(github_bp, url_prefix="/auth")


@app.route('/')
def home():
    if github_bp.is_authenticated:
        resp = github_bp.get("/user")
        user_data = resp.json()
        return render_template('home.html', user=user_data)
    else:
        return render_template('home.html')
    

if __name__ == '__main__':
    app.run(debug=True, 
            host='localhost',  
            port=4444,
            ssl_context=('cert.pem', 'key.pem')) # Per utilizzare HTTPS, aggiungere gli SSL certificates al server