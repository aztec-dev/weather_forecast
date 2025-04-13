# The blueprint containing website routes for weather forecast.
import asyncio
from flask import (
    Blueprint, render_template
)

from weather_forecast.db import get_weather_forecast, get_air_pollution_index, get_geographic_location
from . import city_names
bp = Blueprint('weather_forecast', __name__, url_prefix='/weather_forecast')
status_code = 0

@bp.route("/<city_name>")
def display_weather(city_name=None):
    city_data = asyncio.run(get_geographic_location(city_name))  # mainly to get City names because Open Weather Map api doesn't want to include it in their 3.0 api call >:(
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

    # TODO: Handle no city data available


    city_weather = [weather for weather in weather_data if weather.get("name") == city_name]
    if city_weather:
        return render_template("dashboard.html", city_name=city_name, weather=city_weather, city_names=city_names.get_city_name())
    else:
        return render_template("404.html", message=f"City '{city_name}' not found."), 404
    
@bp.route("/")
def index():
    return render_template("dashboard.html")