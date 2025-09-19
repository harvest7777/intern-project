from models import *
import requests

def fetch_weather(lat: float, lon: float) -> WeatherResponse:
    """
    Fetch current weather data from Open-Meteo for the given latitude and longitude.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  # raises an error if the request failed
    cw = response.json().get("current_weather", {})

    # Map dict -> WeatherResponse model
    return WeatherResponse(
        time=cw["time"],
        interval=cw.get("interval", 900),        # some endpoints include this; default if missing
        temperature=cw["temperature"],
        windspeed=cw["windspeed"],
        winddirection=cw["winddirection"],
        is_day=cw["is_day"],
        weathercode=cw["weathercode"],
    )

if __name__ == "__main__":
    weather = fetch_weather(34.0522, -118.2437)  # Example coordinates for Los Angeles
    print(weather)