"""
A minimal weather forecast web application
Date: 22/03/2025
Author: Azariah Pundari
"""

from flask import Flask

app = Flask(__name__)

@app.route("/")
def weather_forecast():
    return "<h1>Weather Forecast</h1>"