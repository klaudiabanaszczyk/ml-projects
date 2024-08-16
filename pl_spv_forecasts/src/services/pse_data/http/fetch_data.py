from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from io import StringIO
from typing import List

import requests
from pandas import read_csv, date_range, concat, to_datetime, DatetimeIndex, DataFrame
from tqdm.notebook import tqdm


@dataclass
class PseHttp:
    """
    Class for fetching and processing data from PSE HTTP API.

    Attributes
    ----------
    start_date: date
        The start date for the data fetching period.

    end_date: date
        The end date for the data fetching period.
        The maximum date is 13/06/2024, as there is no more recent data.
        Newer data can be downloaded using the PSE API.
    """

    start_date: date = field(default=date(2023, 1, 1))
    end_date: date = field(default=date(2024, 6, 13))

    def __post_init__(self):
        if self.end_date > date(2024, 6, 13):
            self.end_date = date(2024, 6, 13)

    def __str__(self):
        return '\n'.join([f'Start date: {self.start_date}',
                          f'End date: {self.end_date}'])

    def _get_date_range(self) -> List[date]:
        """
        Generate a list of dates at 15-day intervals within the start and end dates.
        """
        return [i.date() for i in date_range(self.start_date, self.end_date, freq='15d')]

    @staticmethod
    def _format_date(_date) -> str:
        """
        Format
        """
        return _date.strftime('%Y%m%d')

    @staticmethod
    def get_response_from_pse_http(start: str, until: str) -> requests.Response:
        """
        Fetching data from PSE HTTP API for the given date range.
        The 'start' and 'until' parameters should be formatted as 'YYYYMMDD'.
        """
        url = f'https://www.pse.pl/getcsv/-/export/csv/PL_GEN_WIATR/data_od/{start}/data_do/{until}'
        return requests.get(url)

    @staticmethod
    def transform_pse_http_response_to_dataframe(response: requests.Response) -> DataFrame:
        """
        Transform API response to pandas DataFrame.
        """

        return read_csv(StringIO(response.content.decode("Windows-1250")), sep=';')

    @staticmethod
    def process_pse_http_data(df: DataFrame) -> DataFrame:
        """
        Process historical data published by PSE via the HTTP service

        Parameters
        ----------
        df: pd.DataFrame
            A DataFrame with source data of PV and wind production fetched using requests from the PSE website.

        Returns
        -------
        pd.DataFrame
            Processed DataFrame with 'pv' and 'wind' columns.
        """
        df.loc[(df['Data'] == '2024-03-31') & (df['Godzina'] == 3), 'Godzina'] = 2
        df = df.rename(columns={'Data': 'date', 'Godzina': 'hour',
                                'Generacja źródeł wiatrowych': 'wind',
                                'Generacja źródeł fotowoltaicznych': 'pv'})
        df['date'] = to_datetime(df['date'])
        df['datetime'] = df.apply(lambda x: datetime(x['date'].year, x['date'].month, x['date'].day, x.hour - 1),
                                  axis=1)
        df = df.set_index('datetime')
        df.index = DatetimeIndex(df.index, tz='CET', ambiguous='infer')
        df = df.replace(',', '.', regex=True)
        df['pv'] = df['pv'].astype(float)
        df['wind'] = df['wind'].astype(float)
        return df[['pv', 'wind']]


def main():
    pse_http = PseHttp()
    dates = pse_http._get_date_range()
    dfs = []
    for i in tqdm(range(len(dates))):
        start = pse_http._format_date(dates[i])
        until = dates[i + 1] - timedelta(1) if i < len(dates) - 1 else pse_http.end_date
        until = pse_http._format_date(until)
        response = pse_http.get_response_from_pse_http(start, until)
        df = pse_http.transform_pse_http_response_to_dataframe(response)
        dfs.append(df)
    concatenated_df = concat(dfs, ignore_index=True)
    return pse_http.process_pse_http_data(concatenated_df)
