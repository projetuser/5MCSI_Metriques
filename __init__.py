from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def mongraphique2():
    return render_template("graphique2.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

DB_NAME = "commits.db"
GITHUB_API_URL = "https://api.github.com/repos/projetuser/5MCSI_Metriques/commits"

# Création de la table si elle n'existe pas
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS commits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            commit_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Récupération des commits depuis GitHub et stockage dans SQLite
def fetch_commits():
    response = urlopen(GITHUB_API_URL)
    commits = json.loads(response.read())

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    for commit in commits:
        commit_time = commit["commit"]["author"]["date"]
        c.execute("INSERT INTO commits (commit_time) VALUES (?)", (commit_time,))

    conn.commit()
    conn.close()

# Exécuter une seule fois au début
init_db()
fetch_commits()

@app.route("/commits/")
def commits():
    conn = sqlite3.connect("commits.db")
    c = conn.cursor()
    c.execute("SELECT commit_time FROM commits")
    commits = c.fetchall()
    conn.close()

    # Convertir les dates en minutes
    commit_minutes = [datetime.strptime(commit[0], "%Y-%m-%dT%H:%M:%SZ").minute for commit in commits]

    # Compter les commits par minute
    commit_counts = Counter(commit_minutes)

    return render_template("commits.html", commit_counts=commit_counts)

if __name__ == "__main__":
  app.run(debug=True)
