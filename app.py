"""
A minimal weather forecast web application
Date: 22/03/2025
Author: Azariah Pundari
"""

from flask import Flask
from flask import render_template
# from markupsafe import escape

app = Flask(__name__)  # Creates an instance of flask

@app.route("/weather_forecast")
def weather_forecast(city=None):
    return render_template('weather_forecast.html')

# @app.route("/<name>")
# def hello(name):
#     return f"<h1>Hello {escape(name)}"