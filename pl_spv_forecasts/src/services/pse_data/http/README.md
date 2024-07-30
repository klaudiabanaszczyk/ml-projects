# HTTP data

## Data Acquisition Method

Data (until June 14, 2024) from the PSE website is acquired using HTTP GET requests and CSV files downloads.

### Query Structure

The request is sent to the following URL, where `start` and `until` are dates in the `YYYYMMDD` format:

```bash
https://www.pse.pl/getcsv/-/export/csv/PL_GEN_WIATR/data_od/{start}/data_do/{until}
```

### Response Structure

The response from the API is in CSV format. An example response might look like this:

```csv
Data;Godzina;Generacja źródeł wiatrowych;Generacja źródeł fotowoltaicznych
2023-07-01;1;100,55;0,00
2023-07-01;2;105,61;0,00
...
2023-07-01;24;20,56;0,00
```