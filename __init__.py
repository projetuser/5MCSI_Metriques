from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
from collections import Counter
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

@app.route('/commits/')
def commits_page():
    return render_template('commits.html')

import requests  # <-- Tu avais oublié cette importation

@app.route('/api/commits-per-minute/')
def extract_commits_per_minute():
    url = 'https://api.github.com/repos/projetuser/5MCSI_Metriques/commits'
    headers = {'User-Agent': 'FlaskApp'}

    response = requests.get(url, headers=headers)
    data = response.json()

    minutes = []
    for commit in data:
        try:
            date_str = commit['commit']['author']['date']
            date_object = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minutes.append(date_object.minute)
        except Exception:
            continue

    compteur = Counter(minutes)
    chart_data = [["Minute", "Commits"]]
    for minute in range(60):
        chart_data.append([str(minute), compteur.get(minute, 0)])

    return jsonify(chart_data)

if __name__ == "__main__":
  app.run(debug=True)
