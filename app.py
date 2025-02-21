from flask import Flask, render_template, request, redirect, url_for, jsonify

import json

import os

from datetime import date

 

app = Flask(__name__)

 

# Database file

DB_FILE = 'stations.json'

 

def load_data():

    if os.path.exists(DB_FILE):

        with open(DB_FILE, 'r') as file:

            return json.load(file)

    return {"stations": []}

 

def save_data(data):

    with open(DB_FILE, 'w') as file:

        json.dump(data, file, indent=4)

 

# Load initial data

data = load_data()

 

@app.route('/')

def index():

    stations = data.get("stations", [])

    return render_template('index.html', stations=stations)

 

@app.route('/update_progress', methods=['POST'])

def update_progress():

    station_id = int(request.form['station_id'])

    progress = request.form['progress']

   

    for station in data['stations']:

        if station['id'] == station_id:

            station['progress'] = progress

            break

   

    save_data(data)

    return redirect(url_for('index'))

 

@app.route('/add_station', methods=['POST'])

def add_station():

    name = request.form['name']

    budget = float(request.form['budget'])

    status_cost = float(request.form['status_cost'])

    saved_money = float(request.form['saved_money'])

    additional_needed = budget - status_cost - saved_money

   

    new_station = {

        "id": len(data['stations']) + 1,

        "name": name,

        "progress": "Not Started",

        "budget": budget,

        "status_cost": status_cost,

        "saved_money": saved_money,

        "additional_needed": additional_needed

    }

    data['stations'].append(new_station)

    save_data(data)

    return redirect(url_for('index'))

 

@app.route('/remove_station', methods=['POST'])

def remove_station():

    station_id = int(request.form['station_id'])

    data['stations'] = [station for station in data['stations'] if station['id'] != station_id]

    save_data(data)

    return redirect(url_for('index'))

 

@app.route('/update_budget', methods=['POST'])

def update_budget():

    station_id = int(request.form['station_id'])

    additional_budget = float(request.form['additional_budget'])

   

    for station in data['stations']:

        if station['id'] == station_id:

            station['budget'] += additional_budget

            station['additional_needed'] = station['budget'] - station['status_cost'] - station['saved_money']

            break

   

    save_data(data)

    return redirect(url_for('index'))

 

@app.route('/update_status_cost', methods=['POST'])

def update_status_cost():

    station_id = int(request.form['station_id'])

    additional_cost = float(request.form['additional_cost'])

   

    for station in data['stations']:

        if station['id'] == station_id:

            station['status_cost'] += additional_cost

            station['additional_needed'] = station['budget'] - station['status_cost'] - station['saved_money']

            break

   

    save_data(data)

    return redirect(url_for('index'))

 

@app.route('/add_saved_money', methods=['POST'])

def add_saved_money():

    station_id = int(request.form['station_id'])

    additional_savings = float(request.form['additional_savings'])

   

    for station in data['stations']:

        if station['id'] == station_id:

            station['saved_money'] += additional_savings

            station['additional_needed'] = station['budget'] - station['status_cost'] - station['saved_money']

            break

   

    save_data(data)

    return redirect(url_for('index'))

 

if __name__ == "__main__":

    app.run(debug=True)