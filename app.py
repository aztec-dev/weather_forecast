"""
A minimal weather forecast web application
Date: 22/03/2025
Author: Azariah Pundari
"""

from flask import Flask, jsonify
from flask import render_template
import requests

app = Flask(__name__)  # Creates an instance of flask

@app.route("/weather_forecast", methods=['GET'])
def get_forecast():
    # Testing API get
    api_key = "310fb733be43977ce18fd565acafd2d0"
    params = ["-11.8092", "51.509865"]
    api_url = f"https://api.openweathermap.org/data/3.0/onecall/overview?lat={params[0]}&lon={params[1]}&appid={api_key}"

    # Make a request
    response = requests.get(api_url)
    if response.status_code == 401:
        weather_data = response.json()
        return jsonify(weather_data)  # Return JSON to the user
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code
