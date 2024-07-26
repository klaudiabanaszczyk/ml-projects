from pandas import read_table,date_range,concat,to_datetime,DatetimeIndex,DataFrame
from datetime import datetime,date,timedelta,tzinfo
import requests
from io import StringIO
from dataclasses import dataclass,field
from typing import List
from tqdm.notebook import tqdm


@dataclass
class PseHttp:
    """
    Class for fetching and processing data from PSE HTTP API.
    
    Attributes:
    start_date (date): The start date for the data fetching period.
    end_date (date): The end date for the data fetching period. 
        The maximum date is 13/06/2024, as there is no more recent data.
        Newer data can be downloaded using the PSE API.
    """
    
    start_date: date = field(default=date(2023,1,1))
    end_date: date = field(default=date(2024,6,13))

    
    def __post_init__(self):
        if self.end_date > date(2024,6,13):
            self.end_date = date(2024,6,13)

    
    def _get_date_range(self) -> List[date]:
        """
        Generate a list of dates at 15-day intervals within the start and end dates.
        """
        return [i.date() for i in date_range(self.start_date, self.end_date, freq='15d')]

    
    def get_response_from_pse_http(self, start: str, until: str) -> requests.Response:
        """
        Fetching data from PSE HTTP API for the given date range.
        The 'start' and 'until' parameters should be formatted as 'YYYYMMDD'.
        """
        url = f'https://www.pse.pl/getcsv/-/export/csv/PL_GEN_WIATR/data_od/{start}/data_do/{until}'
        return requests.get(url)


    def transform_response_to_dataframe(self, dates: List[date], i: int) -> DataFrame:
        """
        Transform API response to pandas DataFrame.
        
        Parameters
        ----------
        dates: List[date]
            List of date ranges.
        i: int
            Index for the current date range.
        """
        start = dates[i].strftime('%Y%m%d')
        until = (dates[i+1]-timedelta(1)).strftime('%Y%m%d') if i < len(dates)-1 else self.end_date.strftime('%Y%m%d')
        response = self.get_response_from_pse_http(start,until)
        return read_table(StringIO(response.content.decode('ansi')), sep=';')
    
    
    def fetch_noprocessed_pse_data(self) -> DataFrame:
        """
        Fetch raw data from PSE for the defined date range.
        """
        dates = self._get_date_range()
        dfs = []
        for i in tqdm(range(len(dates))):
            df = self.transform_response_to_dataframe(dates, i)
            dfs.append(df)
        return concat(dfs)

    def fetch_processed_pse_data(self):
        """
        Fetch and process data from PSE.
        
        Returns
        -------
        DataFrame
            Processed DataFrame with 'pv' and 'wind' columns.
        """
        df = self.fetch_noprocessed_pse_data()
        df.loc[(df['Data'] == '2024-03-31')&(df['Godzina'] == 3), 'Godzina'] = 2
        df = df.rename(columns={'Data': 'date', 'Godzina': 'hour',
                                'Generacja źródeł wiatrowych': 'wind',
                                'Generacja źródeł fotowoltaicznych': 'pv'})
        df['date'] = to_datetime(df['date'])
        df['datetime'] = df.apply(lambda x: datetime(x['date'].year, x['date'].month, x['date'].day, x.hour-1), axis=1)
        df = df.set_index('datetime')
        df.index = DatetimeIndex(df.index, tz='CET', ambiguous='infer')
        df = df.replace(',','.',regex=True)
        df['pv'] = df['pv'].astype(float)
        df['wind'] = df['wind'].astype(float)
        return df[['pv','wind']]