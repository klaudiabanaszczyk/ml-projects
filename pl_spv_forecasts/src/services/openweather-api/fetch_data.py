from dataclasses import dataclass
import requests


@dataclass
class OpenWeatherForecasts:
    """
    A class to retrieve forecast weather data from the OpenWeather API.    
    """

    base_url = 'https://api.openweathermap.org/data/3.0/onecall?'

    def call_openweather_api(self, lat: float, lon: float, api_key: str) -> requests.Response:
        return requests.get(f'{self.base_url}lat={lat}&lon={lon}&exclude=minutely,daily&appid={api_key}')


    def fetch_openweather_forecast_data(self, api_response):
        pass


@dataclass
class OpenWeatherArchiveData:
    """
    A class to retrieve historical weather data from the OpenWeather API.
    """

    base_url = 'https://api.openweathermap.org/data/3.0/timemachine?'

    def call_openweather_api(self, lat: float, lon: float, time: int, api_key: str) -> requests.Response:
        return requests.get(f'{self.base_url}lat={lat}&lon={lon}&dt={time}&appid={api_key}')

    def fetch_openweather_archive_data(self, api_response):
        pass
