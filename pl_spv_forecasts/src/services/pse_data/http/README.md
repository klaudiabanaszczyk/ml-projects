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

### Required Libraries

To run the code and perform data acquisition and processing, you need to install the following Python libraries:

1. **requests**: To perform HTTP GET requests.
2. **pandas**: To handle CSV data and perform data manipulation.
3. **tqdm**: To provide a progress bar for loops (optional, for better visualization).

You can install these libraries using pip if you haven’t already:
```bash
pip install requests pandas tqdm
```

### How to Run the Code
1. Save the code to a file, for example, pse_data_acquisition.py.
2. Run the script using Python from your terminal or command prompt:

```bash
python pse_data_acquisition.py
```
