from dataclasses import dataclass
from datetime import datetime
import requests
from pandas import DataFrame, DatetimeIndex


@dataclass
class OpenWeatherForecasts:
    """
    A class to retrieve forecast weather data from the OpenWeather API.
    """

    base_url = 'https://api.openweathermap.org/data/3.0/onecall?'

    def call_openweather_api(self, lat: float, lon: float, api_key: str) -> requests.Response:
        """
        Sends an HTTP GET request to the OpenWeather API to retrieve forecast weather data for a specified
        geographic location.

        Parameters:
        -----------
        lat: float
            Latitude of the location for which the weather data is to be retrieved.
        lon: float
            Longitude of the location for which the weather data is to be retrieved.
        api_key: str
            API key used to authenticate access to the OpenWeather service.

        Returns:
        --------
        requests.Response
            HTTP response object containing the weather data for the specified location.
        """
        return requests.get(f'{self.base_url}lat={lat}&lon={lon}&exclude=minutely,daily&appid={api_key}')

    @staticmethod
    def fetch_openweather_forecast_data(api_response: requests.Response) -> DataFrame:
        """
        Processes the JSON response from the OpenWeather API and converts the hourly forecast data
        into a Pandas DataFrame.

        Parameters:
        -----------
        api_response : requests.Response
            The HTTP response object returned from the OpenWeather API containing the forecast data
            in JSON format.

        Returns:
        --------
        DataFrame
            A Pandas DataFrame containing the hourly weather forecast. The DataFrame includes
            additional metadata columns for latitude, longitude, timezone, and publication date.
            The index is set to the forecast datetime in UTC.
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

    def call_openweather_api(self, lat: float, lon: float, start_time: int, end_time: int,
                             api_key: str) -> requests.Response:
        return requests.get(
            f'{self.base_url}lat={lat}&lon={lon}&type=hour&start={start_time}&end={end_time}&appid={api_key}')

    @staticmethod
    def transform_datetime_to_timestamp(_date: datetime) -> int:
        return int(datetime.timestamp(_date))

    def fetch_openweather_archive_data(self, api_response):
        pass


def forecast_main():
    forecasts = OpenWeatherForecasts()
    response = forecasts.call_openweather_api(52.286, 20.8, '')
    data = forecasts.fetch_openweather_forecast_data(response)
    return data
