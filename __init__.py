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

@app.route('/commits/')
def commits():
    url = 'https://api.github.com/repos/projetuser/5MCSI_Metriques/commits'
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))

    # Extraire les minutes des commits
    commit_minutes = []
    for commit in data:
        commit_date = commit['commit']['author']['date']
        # Convertir la date et extraire la minute
        date_object = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
        commit_minutes.append(date_object.minute)

    # Comptabiliser le nombre de commits par minute
    minute_count = {minute: commit_minutes.count(minute) for minute in set(commit_minutes)}

    return render_template('commits.html', minute_count=minute_count)

if __name__ == "__main__":
  app.run(debug=True)
