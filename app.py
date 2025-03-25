"""
A minimal weather forecast web application
Date: 22/03/2025
Author: Azariah Pundari
"""

import os
from flask import Flask, jsonify
from flask import render_template
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)  # Creates an instance of flask

@app.get("/weather_forecast")
def get_forecast():
    # Testing API get
    api_key = os.getenv("OPEN_WEATHER_MAP_API_KEY")
    cities = ["Brisbane", "Townsville", "Cairns", "Port Moresby"]
    data = []
    for city in cities:
        api_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
        response = requests.get(api_url)
        geo_location = response.json()
        for city_data in geo_location:
            required_data = {
                "name": city_data['name'],
                "lon": city_data['lon'],
                "lat": city_data['lat']
            }
            data.append(required_data)

    # Make a request
    if response.status_code == 200:
        # weather_data = data.json()
        return render_template("weather_forecast.html", weather=data)  # Return JSON to the user
    else:
        return jsonify({"error": "Failed to fetch data"}), geo_location.status_code