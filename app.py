
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)

@app.route('/start')
def start():
    return render_template('start.html')

app.secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key')

DB_PATH = 'Baum.db'
USERS = {'benutzer1': 'geheim123'}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if USERS.get(username) == password:
            session['username'] = username
            return redirect(url_for('baum_suche'))
        else:
            return render_template('login.html', fehler="Falscher Benutzername oder Passwort.")
    return render_template('login.html')

@app.route('/baum', methods=['GET', 'POST'])
def baum_suche():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        uid = request.form['uid']
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM imported_data WHERE UID=?", (uid,))
        baum = cur.fetchone()
        conn.close()
        if baum:
            return render_template('baum_ergebnis.html', baum=baum)
        else:
            return render_template('baum_suche.html', fehler="UID nicht gefunden.")
    return render_template('baum_suche.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
