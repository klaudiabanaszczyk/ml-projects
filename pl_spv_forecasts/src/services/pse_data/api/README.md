# API data

## Data Acquisition Method

Data (from June 14, 2024) from the PSE website is acquired using the API as documented on the site: [https://api.raporty.pse.pl/](https://api.raporty.pse.pl/)

### Query Structure

API queries are made by sending HTTP GET requests to specific endpoints. Example endpoint:

```bash
https://api.raporty.pse.pl/api/{entity}?$filter=doba eq {date}
```
- `entity`: name of the report, a full list of report names can be found on the website: [https://api.raporty.pse.pl/](https://api.raporty.pse.pl/).
- `date`: date of energy delivery, despite the ability to declare a date range, the eq (equals) parameter was used because of the limits of the rows returned by API

### Response Structure

The returned result is a JSON object in the following format:

```bash
{
    "value": []
}
```

For example:

```bash
{
    "value": [
        {
            "jg": 12132.16,
            "pv": 0.524,
            "wi": 291.313,
            "jgm": -15.179,
            "doba": "2024-06-14",
            "udtczas": "2024-06-14 00:15",
            "udtczas_oreb": "00:00 - 00:15",
            "business_date": "2024-06-14",
            "source_datetime": "2024-07-18 19:20:46.357",
            "zapotrzebowanie": 16284.849
        },
        {
            "jg": 11786.202,
            "pv": 0.525,
            "wi": 311.635,
            "doba": "2024-06-14",
            "udtczas": "2024-06-14 00:30",
            "udtczas_oreb": "00:15 - 00:30",
            "business_date": "2024-06-14",
            "source_datetime": "2024-07-18 19:20:46.357",
            "zapotrzebowanie": 15954.67
        }
    ]
}
```

## Error handling

The API can return various HTTP status codes indicating errors:
- 400 Bad Request: Invalid request (e.g., missing required parameters).
- 404 Not Found: Resources not found (e.g., invalid endpoint).
- 500 Internal Server Error: Server-side error.

## Requirements and limitations

- No API key is required.
- No query limits.
