# The blueprint containing website routes for weather forecast.
import asyncio
from flask import (
    Blueprint, render_template
)

from weather_forecast.db import get_weather_forecast, get_air_pollution_index, get_geographic_location

bp = Blueprint('weather_forecast', __name__, url_prefix='/weather_forecast')

@bp.route("/forecast")
@bp.route("/forecast/<city_name>")
def display_weather(city_name=None):
    city_data = asyncio.run(get_geographic_location(city_name))
    weather_data = asyncio.run(get_weather_forecast(city_name))
    air_pollution_index = asyncio.run(get_air_pollution_index(city_name))

    # Map city data with air pollution index
    for city in city_data:
        for pollution in air_pollution_index:
            if city['lat'] == pollution['lat'] and city['lon'] == pollution['lon']:
                city['aqi'] = pollution['aqi']

    # Link city names and AQI to weather data
    for weather in weather_data:
        for city in city_data:
            if weather['lat'] == city['lat'] and weather['lon'] == city['lon']:
                weather['name'] = city['name']
                weather['aqi'] = city.get('aqi', "No AQI data")

    if city_name is None or city_name.lower() == "all cities":
        return render_template("dashboard.html", city_name="All Cities", weather=weather_data, all_cities=[city["name"] for city in city_data])

    city_weather = [weather for weather in weather_data if weather.get("name") == city_name]
    if city_weather:
        return render_template("dashboard.html", city_name=city_name, weather=city_weather, all_cities=[city["name"] for city in city_data])