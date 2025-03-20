from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask(__name__)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4444)
    