from dataclasses import dataclass, field
from datetime import date
from typing import List

import requests
from pandas import DataFrame, Series, to_datetime

from .utils import columns as selected_columns


@dataclass
class VisualCrossingData:
    """
    A class to retrieve and process forecast weather data from the VisualCrossing Weather API.
    """

    base_url: str = field(default='https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/')
    resource_url: str = field(default='timeline')

    def call_visualcrossing_api(self, latitude: float, longitude: float, api_key: str,
                                start_date: date = None, end_date: date = None) -> requests.Response:
        """
        Calls the VisualCrossing Weather API to retrieve weather data for a specific location.

        Parameters
        ----------
        latitude : float
            Latitude of the location.
        longitude : float
            Longitude of the location.
        api_key : str
            API key for accessing the VisualCrossing Weather API.
        start_date : date, optional
            Start date for the weather data (default is None).
        end_date : date, optional
            End date for the weather data (default is None).

        Returns
        -------
        requests.Response
            The HTTP response object containing the weather data.
        """
        url = ''.join([
            f'{self.base_url}{self.resource_url}/{latitude},{longitude}',
            f'/{start_date:%Y-%m-%d}/{end_date:%Y-%m-%d}' if start_date is not None or end_date is not None else '',
            f'?unitGroup=metric&key={api_key}'
        ])
        return requests.get(url)

    @staticmethod
    def _extract_hourly_weather_data(day_data: Series) -> List[dict]:
        """
        Extracts hourly weather data from a single day's weather information.

        Parameters
        ----------
        day_data : Series
            A pandas Series object containing weather data for a specific day.

        Returns
        -------
        list of dict
            A list of dictionaries where each dictionary represents the weather data for a specific hour.
        """
        return [
            {**hour_info,
             'date': day_data['datetime'],
             'sunrise_time': day_data['sunrise'],
             'sunset_time': day_data['sunset']}
            for hour_info in day_data['hours']
        ]

    def fetch_visualcrossing_data(self, response: requests.Response) -> DataFrame:
        """
        Processes the weather data retrieved from the VisualCrossing API and returns it as a pandas DataFrame.

        Parameters
        ----------
        response : requests.Response
            The HTTP response object containing the weather data.

        Returns
        -------
        DataFrame
            A pandas DataFrame containing the processed weather data with the specified columns.
        """
        response_json = response.json()
        daily_data = DataFrame(response_json['days'])
        hourly_data = [self._extract_hourly_weather_data(day_data) for _, day_data in daily_data.iterrows()]
        flattened_data = [hour for sublist in hourly_data for hour in sublist]

        df = DataFrame(flattened_data)
        df['latitude'] = response_json['latitude']
        df['longitude'] = response_json['longitude']
        df['timezone'] = response_json['timezone']
        df['datetime'] = to_datetime(df['date'] + ' ' + df['time'], utc=True)

        return df[selected_columns].rename(columns={'datetime': 'time'})


def main():
    vc = VisualCrossingData()
    response = vc.call_visualcrossing_api(52.4, 21.2, '',
                                          date(2023, 5, 1),
                                          date(2023, 5, 31))
    return vc.fetch_visualcrossing_data(response)
