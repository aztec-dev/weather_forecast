# Acts as a database. Gets data from Open Weather Map using their API and stores locally.
import os
import aiohttp
import asyncio
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

# Load environment variables
load_dotenv()
api_key = os.getenv("OPEN_WEATHER_MAP_API_KEY")

# Asynchronous helper function
async def fetch_data(session, url):
    async with session.get(url) as response:
        return await response.json()


# Get geographic location of cities
async def get_geographic_location():
    cities = ["Brisbane", "Townsville", "Cairns", "Port Moresby", "Paris"]
    data = []

    async with aiohttp.ClientSession() as session:
        tasks = []
        for city in cities:
            geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
            tasks.append(fetch_data(session, geocoding_url))  # Create tasks for each city

        responses = await asyncio.gather(*tasks)

        for geo_location in responses:
            for city_data in geo_location:
                required_data = {
                    "name": city_data['name'],
                    "lon": city_data['lon'],
                    "lat": city_data['lat']
                }
                data.append(required_data)

    return data


# Get air pollution index
async def get_air_pollution_index():
    data = await get_geographic_location()
    required_data = []

    async with aiohttp.ClientSession() as session:
        tasks = []
        for city in data:
            air_pollution_api_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={city['lat']}&lon={city['lon']}&appid={api_key}"
            tasks.append(fetch_data(session, air_pollution_api_url))  # Create tasks for each city

        responses = await asyncio.gather(*tasks)  # Fetch air pollution data concurrently

        for city, air_pollution in zip(data, responses):
            air_pollution_index = {
                "lat": city["lat"],
                "lon": city["lon"],
                "aqi": air_pollution["list"][0]["main"]["aqi"] if "list" in air_pollution and len(air_pollution["list"]) > 0 else "No AQI data"
            }
            required_data.append(air_pollution_index)

    return required_data

# Get weather data
async def get_weather_forecast():
    data = await get_geographic_location()
    air_pollution_index = await get_air_pollution_index()
    weather_data = []

    async with aiohttp.ClientSession() as session:
        tasks = []
        for city in data:
            weather_forecast_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={city['lat']}&lon={city['lon']}&exclude=minutely,hourly,alerts&units=metric&appid={api_key}"
            tasks.append(fetch_data(session, weather_forecast_url))  # Create tasks for each city

        responses = await asyncio.gather(*tasks)  # Fetch weather data concurrently

        for city, weather_forecast in zip(data, responses):
            required_data = {
                "lat": city["lat"],
                "lon": city["lon"],
                "name": city["name"]
            }
            pollution = next((item for item in air_pollution_index if item['lat'] == city['lat'] and item['lon'] == city['lon']), None)
            city_aqi = pollution['aqi'] if pollution else "No AQI data"

            # Current weather
            if "current" in weather_forecast:
                required_data["temp"] = int(round(weather_forecast["current"]["temp"], 2))
                required_data["humidity"] = weather_forecast["current"]["humidity"]
                required_data["visibility"] = weather_forecast["current"]["visibility"]
                required_data["weather_id"] = weather_forecast["current"]["weather"][0]["id"]
                required_data["weather_main"] = weather_forecast["current"]["weather"][0]["main"]
                required_data["weather_description"] = weather_forecast["current"]["weather"][0]["description"]
                required_data["icon"] = weather_forecast["current"]["weather"][0]["icon"]

            # Timezone data
            if "timezone_offset" in weather_forecast:
                timezone_offset = weather_forecast["timezone_offset"]
                current_utc_time = datetime.now(timezone.utc)
                local_time = current_utc_time + timedelta(seconds=timezone_offset)
                required_data["local_time"] = local_time.strftime("%H:%M")
                required_data["day_of_week"] = local_time.strftime("%A")

            # Daily weather forecast
            if "daily" in weather_forecast:
                daily_forecast = []
                for day_data in weather_forecast["daily"]:
                    sunrise_local = datetime.fromtimestamp(day_data["sunrise"] + timezone_offset, timezone.utc)
                    sunset_local = datetime.fromtimestamp(day_data["sunset"] + timezone_offset, timezone.utc)
                    day_data_processed = {
                        "date": datetime.fromtimestamp(day_data["dt"]).strftime("%Y-%m-%d"),
                        "temp_min": int(round(day_data["temp"]["min"], 2)),
                        "temp_max": int(round(day_data["temp"]["max"], 2)),
                        "wind_speed": int(round(day_data["wind_speed"], 2)),
                        "wind_deg": int(round(day_data["wind_deg"], 2)),
                        "weather_description": day_data["weather"][0]["description"],
                        "sunrise": sunrise_local.strftime("%I:%M %p"),
                        "sunset": sunset_local.strftime("%I:%M %p"),
                        "rain": day_data.get("rain", 0),
                        "uvi": day_data["uvi"],
                        "aqi": city_aqi
                    }
                    daily_forecast.append(day_data_processed)

                required_data["daily"] = daily_forecast

            weather_data.append(required_data)
    # print(weather_data)
    return weather_data