from pandas import DataFrame,concat,date_range,to_datetime,DatetimeIndex
from datetime import date,timedelta
from dataclasses import dataclass,field
import requests
from ...exceptions.pse_service_exceptions import StatusCodeNot200


@dataclass
class PseApi:
    """
    Class for interacting with the Polskie Sieci Elektroenergetyczne (PSE) API to fetch basic KSE data.
    """
    
    start_date: date = field(default=date(2024,6,14))
    end_date: date = field(default=date.today()-timedelta(1))
    entity: str = field(default='his-wlk-cal')
    

    def fetch_pse_daily_data(self, selected_date: date) -> DataFrame:
        """
        Fetches daily data from the PSE API for the specified date.

        Parameters
        ----------
        selected_date: date
            The date for which to fetch the data.

        Returns
        -------
        DataFrame
            A DataFrame containing the fetched data with a datetime index.

        Raises
        ------
        StatusCodeNot200
            If the API request returns a non-200 status code.
        """
        url = f"https://api.raporty.pse.pl/api/{self.entity}?$filter=doba eq '{selected_date}'"
        response = requests.get(url)
        try:
            df = DataFrame(response.json()['value'])
            df['datetime'] = DatetimeIndex(to_datetime(df['udtczas']), tz='CET')
            df = df.set_index('datetime')
            df = df.sort_index()
            return df
        except:
            raise StatusCodeNot200(response.status_code, response.reason)


    def fetch_pse_data(self):
        """
        Fetches data from the PSE API for the range of the given dates.
        """
        dates = [d.strftime('%Y-%m-%d') for d in date_range(self.start_date, self.end_date, freq='D')]
        dfs = [self.fetch_pse_daily_data(selected_date) for selected_date in dates]
        return concat(dfs)