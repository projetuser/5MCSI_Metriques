from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
from collections import Counter
                                                                                                                                       
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
def commits():
    # Récupérer les commits depuis l'API de GitHub
    url = 'https://api.github.com/repos/projetuser/5MCSI_Metriques/commits'
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    
    # Extraire les minutes des commits
    commit_minutes = []
    for commit in data:
        commit_date = commit['commit']['author']['date']
        # Convertir la date pour en extraire les minutes
        commit_datetime = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
        commit_minutes.append(commit_datetime.strftime('%Y-%m-%d %H:%M'))  # Format : '2024-02-11 11:57'
    
    # Compter le nombre de commits par minute
    commit_count = Counter(commit_minutes)

    # Convertir en une liste pour envoyer au template
    commit_data = [{'minute': minute, 'count': count} for minute, count in commit_count.items()]
    
    return render_template('commits.html', commit_data=commit_data)

if __name__ == "__main__":
  app.run(debug=True)
