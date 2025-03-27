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
api_key = os.getenv("OPEN_WEATHER_MAP_API_KEY")
app = Flask(__name__)  # Creates an instance of flask

def get_geographic_location():
    # Testing API get

    cities = ["Brisbane", "Townsville", "Cairns", "Port Moresby"]
    data = []
    for city in cities:
        geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
        response = requests.get(geocoding_url)
        geo_location = response.json()
        for city_data in geo_location:
            required_data = {
                "name": city_data['name'],
                "lon": city_data['lon'],
                "lat": city_data['lat']
            }
            data.append(required_data)
    return data

def get_weather():
    data = get_geographic_location()
    weather_data = []
    for city in data:
        weather_forecast_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={city['lat']}&lon={city['lon']}&units=metric&appid={api_key}"
        response = requests.get(weather_forecast_url)
        weather_forecast = response.json()

        if "current" in weather_forecast:
            required_data = {
                "temp": weather_forecast["current"]["temp"],  # Temperature
                "humidity": weather_forecast["current"]["humidity"],  # Humidity
                "lat": city["lat"],
                "lon": city["lon"],
                "name": city["name"]  # Include city name from geolocation data
            }
            weather_data.append(required_data)
    return weather_data


@app.route("/weather_forecast")
@app.route("/weather_forecast/<city_name>")
def display_weather(city_name=None):
    data = get_geographic_location()  # get the data to display city name
    weather_data = get_weather()
    for weather in weather_data:
        for city in data:
            if weather['lat'] == city['lat'] and weather['lon'] == city['lon']:
                weather['name'] = city['name']  # Add name to weather data

    if city_name:  # Display data based on a specific city name
        city_weather = [weather for weather in weather_data if weather.get("name") == city_name]
        if city_weather:
            return render_template("weather_forecast.html", city_name=city_name, weather=city_weather)
        else:
            return render_template("weather_forecast.html", city_name="Unknown", weather=[])
    else:  # Display all cities' weather data
        return render_template("weather_forecast.html", city_name="All Cities", weather=weather_data)
