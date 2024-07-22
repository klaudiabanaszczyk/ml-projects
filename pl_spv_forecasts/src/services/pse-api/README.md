# Data Source

The data used in this project regarding actual values from the energy market are sourced from the official website of Polskie Sieci Elektroenergetyczne (PSE):

[https://www.pse.pl/home](https://www.pse.pl/home)

The website presents data on planned and current power flows in Poland, the demand and supplied power from various energy sources, as well as forecasted and settlement prices from the balancing market and additional services provided by PSE.

# Data Acquisition Method

Data from the PSE website is acquired using the API as documented on the site: [https://api.raporty.pse.pl/](https://api.raporty.pse.pl/)

## Query Structure

API queries are made by sending HTTP GET requests to specific endpoints. Example endpoint:

```bash
https://api.raporty.pse.pl/api/{entity}?
- `entity`: name of the report, a full list of report names can be found on the website: [https://api.raporty.pse.pl/](https://api.raporty.pse.pl/).

... TBC ...