"""
A minimal weather forecast web application
Date: 22/03/2025
Author: Azariah Pundari
"""

from flask import Flask
from markupsafe import escape

app = Flask(__name__)  # Creates an instance of flask

@app.route("/")
def weather_forecast():
    return "<h1>Weather Forecast</h1>"

@app.route("/<name>")
def hello(name):
    return f"<h1>Hello {escape(name)}"