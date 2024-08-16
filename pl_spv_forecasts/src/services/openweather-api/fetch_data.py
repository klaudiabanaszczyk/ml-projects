from pandas import DataFrame, DatetimeIndex
from datetime import datetime, date, timedelta
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

    def fetch_openweather_forecast_data(self, api_response: requests.Response) -> DataFrame:
        """

        """
        response_json = api_response.json()
        df = DataFrame(response_json['hourly'])
        df['lat'] = response_json['lat']
        df['lon'] = response_json['lon']
        df['timezone'] = response_json['timezone']
        df['dt'] = df['dt'].apply(datetime.fromtimestamp)
        df.index = DatetimeIndex(df['dt']).tz_localize('UTC')
        df.index.name = 'datetime'
        df['publication_date'] = datetime.now()
        return df


@dataclass
class OpenWeatherArchiveData:
    """
    A class to retrieve historical weather data from the OpenWeather API.
    """

    base_url = 'https://history.openweathermap.org/data/2.5/history/city?'

    def transform_datetime_to_timestampt(self, _date: datetime) -> int:
        return int(datetime.timestamp(_date))

    def call_openweather_api(self, lat: float, lon: float, start_time: int, end_time: int,
                             api_key: str) -> requests.Response:
        return requests.get(
            f'{self.base_url}lat={lat}&lon={lon}&type=hour&start={start_time}&end={end_time}&appid={api_key}')

    def fetch_openweather_archive_data(self, api_response):
        pass


def forecast_main():
    api_key = ''
    lat = 52.286
    lon = 20.8

    forecasts = OpenWeatherForecasts()
    response = forecasts.call_openweather_api(lat, lon, api_key)
    data = forecasts.fetch_openweather_forecast_data(response)
    return data