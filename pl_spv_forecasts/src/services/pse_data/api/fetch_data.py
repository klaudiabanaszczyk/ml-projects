from pandas import DataFrame,concat,date_range,to_datetime,DatetimeIndex
from datetime import date,timedelta
from dataclasses import dataclass,field
import requests
from pl_spv_forecasts.src.exceptions.pse_service_exceptions import StatusCodeNot200


@dataclass
class PseApi:
    """
    Class for interacting with the Polskie Sieci Elektroenergetyczne (PSE) API to fetch basic KSE data.
    """

    start_date: date = field(default=date(2024,6,14))
    end_date: date = field(default=date.today()-timedelta(1))
    entity: str = field(default='his-wlk-cal')

    
    def call_pse_api(self, selected_date: date) -> DataFrame:
        """
        Gets response from the PSE API for the specified date.

        Parameters
        ----------
        selected_date: date
            The date for which to fetch the data.

        Returns
        -------
        dict
            The response from the PSE API.
        """
        url = f"https://api.raporty.pse.pl/api/{self.entity}?$filter=doba eq '{selected_date}'"
        return requests.get(url)

    
    def _api_response_to_dataframe (self, selected_date: date) -> DataFrame:
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
        response = self.call_pse_api(selected_date)
        match response.status_code:
            case 200:
                df = DataFrame(response.json()['value'])
                df['datetime'] = DatetimeIndex(to_datetime(df['udtczas']), tz='CET')
                df = df.set_index('datetime')
                df = df.sort_index()
                return df
            case _:
                raise StatusCodeNot200(response.status_code, response.reason)


    def fetch_pse_data(self) -> DataFrame:
        """
        Fetches data from the PSE API for the range of the given dates.
        """
        dates = [d.strftime('%Y-%m-%d') for d in date_range(self.start_date, self.end_date, freq='D')]
        dfs = [self._api_response_to_dataframe (selected_date) for selected_date in dates]
        return concat(dfs)