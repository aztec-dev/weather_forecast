import os
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import requests

# Load environment variables
load_dotenv()
api_key = os.getenv("OPEN_WEATHER_MAP_API_KEY")
app = Flask(__name__)  # Creates an instance of flask

def get_geographic_location():
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
        # Fetch weather forecast data including hourly and daily forecasts
        weather_forecast_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={city['lat']}&lon={city['lon']}&units=metric&appid={api_key}"
        response = requests.get(weather_forecast_url)
        weather_forecast = response.json()

        required_data = {
            "lat": city["lat"],
            "lon": city["lon"],
            "name": city["name"],  # Include city name from geolocation data
        }

        # Get current weather
        if "current" in weather_forecast:
            required_data["temp"] = int(round(weather_forecast["current"]["temp"], 2))  # Temperature
            required_data["humidity"] = weather_forecast["current"]["humidity"]  # Humidity

        # Get timezone data
        if "timezone_offset" in weather_forecast:
            timezone_offset = weather_forecast["timezone_offset"]
            current_utc_time = datetime.now(timezone.utc)
            local_time = current_utc_time + timedelta(seconds=timezone_offset)
            required_data["local_time"] = local_time.strftime("%I:%M %p")

        # Get daily weather forecast (daily summary)
        if "daily" in weather_forecast:
            daily_forecast = []
            for day_data in weather_forecast["daily"]:
                day_data_processed = {
                    "date": datetime.fromtimestamp(day_data["dt"]).strftime("%Y-%m-%d"),
                    "temp_min": int(round(day_data["temp"]["min"], 2)),
                    "temp_max": int(round(day_data["temp"]["max"], 2)),
                    "wind_speed": int(round(day_data["wind_speed"], 2)),
                    "wind_deg": int(round(day_data["wind_deg"], 2)),
                    "weather_description": day_data["weather"][0]["description"],
                    "rain": day_data.get("rain", 0),  # Rain over the day
                }
                daily_forecast.append(day_data_processed)

            required_data["daily"] = daily_forecast

        weather_data.append(required_data)
        print(weather_data[-1])  # Print the last item added to weather_data for debugging

    return weather_data

@app.route("/weather_forecast")
@app.route("/weather_forecast/<city_name>")
def display_weather(city_name=None):
    city_data = get_geographic_location()
    weather_data = get_weather()

    # Link city names to weather data
    for weather in weather_data:
        for city in city_data:
            if weather['lat'] == city['lat'] and weather['lon'] == city['lon']:
                weather['name'] = city['name']

    if city_name:  # Show weather for a specific city
        city_weather = [weather for weather in weather_data if weather.get("name") == city_name]
        return render_template("weather_forecast.html", city_name=city_name, weather=city_weather, all_cities=[city["name"] for city in city_data])
    else:  # Show all cities
        return render_template("weather_forecast.html", city_name="All Cities", weather=weather_data, all_cities=[city["name"] for city in city_data])
