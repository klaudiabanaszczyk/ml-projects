from pandas import DataFrame, Series, concat, to_datetime
from datetime import date
import requests
from dataclasses import dataclass
from utils import columns as selected_columns


@dataclass
class VisualCrossingData:
    """
    A class to retrieve forecast weather data from the VisualCrossing Weather API.
    """

    base_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'

    def call_visualcrossing_api(self, lat: float, lon: float, api_key: str,
                                start_date: date = None, end_date: date = None) -> requests.Response:
        if start_date is None or end_date is None:
            return requests.get(f'{self.base_url}/{lat},{lon}?unitGroup=metric&key={api_key}')
        else:
            start = start_date.strftime('%Y-%m-%d')
            until = end_date.strftime('%Y-%m-%d')
            return requests.get(f'{self.base_url}/{lat},{lon}/{start}/{until}?unitGroup=metric&key={api_key}')

    @staticmethod
    def _extract_hours_data(row: Series) -> DataFrame:
        df = DataFrame(row['hours'])
        df['date'] = row['datetime']
        df['sunrise_time'] = row['sunrise']
        df['sunset_time'] = row['sunset']
        return df

    def fetch_visualcrossing_data(self, response: requests.Response) -> DataFrame:
        response_json = response.json()
        source_data = DataFrame(response_json['days'])
        df = concat([self._extract_hours_data(r) for _, r in source_data.iterrows()])
        df['lat'] = response_json['latitude']
        df['lon'] = response_json['longitude']
        df['timezone'] = response_json['timezone']
        df['datetime'] = to_datetime(df['date'] + ' ' + df['time'], utc=True)
        return df[selected_columns].rename(columns={'datetime': 'time'})


def main():
    vc = VisualCrossingData()
    response = vc.call_visualcrossing_api(52.4, 21.2, '',
                                          date(2023, 5, 1),
                                          date(2023, 5, 31))
    return vc.fetch_visualcrossing_data(response)
