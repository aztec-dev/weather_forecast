import os
from flask import Flask
from dotenv import load_dotenv
from . import weather

# Load environment variables
load_dotenv()
api_key = os.getenv("OPEN_WEATHER_MAP_API_KEY")

def create_app(test_config=None):
    app = Flask(__name__)  # Creates an instance of flask
    app.register_blueprint(weather.bp)

    @app.route('/hello')
    def hello():
        return "Hello, World!"

    return app