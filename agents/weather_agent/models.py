from uagents import Model, Field
from datetime import datetime

class WeatherQuery(Model):
    latitude: float = Field(
        ...,
        description="Geographic latitude in decimal degrees (-90 to 90; positive = North, negative = South)"
    )
    longitude: float = Field(
        ...,
        description="Geographic longitude in decimal degrees (-180 to 180; positive = East, negative = West)"
    )


class WeatherResponse(Model):
    time: datetime = Field(
        ...,
        description="ISO 8601 timestamp of the weather observation (e.g. 2025-09-18T18:15:00)"
    )
    interval: int = Field(
        ...,
        description="Validity duration of the weather data in seconds (e.g. 900 = 15 minutes)"
    )
    temperature: float = Field(
        ...,
        description="Air temperature in Celsius (float, can be negative)"
    )
    windspeed: float = Field(
        ...,
        description="Wind speed in kilometers per hour (float, >=0)"
    )
    winddirection: int = Field(
        ...,
        description="Wind direction in degrees (integer, 0 = North, 90 = East, 180 = South, 270 = West)"
    )
    is_day: int = Field(
        ...,
        description="Daylight indicator (1 = day, 0 = night)"
    )
    weathercode: int = Field(
        ...,
        description="Weather condition code (integer; e.g. 0=Clear, 1=Mainly clear, 2=Partly cloudy, 3=Overcast, 45=Fog, 61=Rain, etc.)"
    )
