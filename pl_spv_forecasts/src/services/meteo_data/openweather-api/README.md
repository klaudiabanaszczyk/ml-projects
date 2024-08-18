# OpenWeather API

## Data Acquisition Method

Data from the OpenWeather platform is acquired using the API as documented on the site: [https://openweathermap.org/api/one-call-3](https://api.raporty.pse.pl/)

### Query Structure

API queries are made by sending HTTP GET requests to specific endpoints. Example endpoint:

```bash
https://api.openweathermap.org/data/3.0/onecall/overview?lat={lat}&lon={lon}&appid={api_key}
```
- `lat`: The latitude of the location. Replace {lat} with the actual latitude value (e.g., 52.52).
- `lon`: The longitude of the location. Replace {lon} with the actual longitude value (e.g., 23.405).
- `api_key`: Your unique API key. Replace {api_key} with the key you obtained from OpenWeather.

### Response Structure

The response returned by the API is a JSON object in the format that can be found on the website: [https://openweathermap.org/api/one-call-3#example](https://api.raporty.pse.pl/)
Below you can find an example of the API response format for hourly data:

```bash
{{'lat': 52.286,
 'lon': 20.8,
 'timezone': 'Europe/Warsaw',
 'timezone_offset': 7200,
 'hourly': [{'dt': 1724004000,
   'temp': 300.12,
   'feels_like': 301.26,
   'pressure': 1006,
   'humidity': 61,
   'dew_point': 291.96,
   'uvi': 0,
   'clouds': 20,
   'visibility': 10000,
   'wind_speed': 1.22,
   'wind_deg': 197,
   'wind_gust': 1.88,
   'weather': [{'id': 801,
     'main': 'Clouds',
     'description': 'few clouds',
     'icon': '02n'}],
   'pop': 0},
  ...],
 'alerts': [{'sender_name': 'IMGW-PIB Centralne Biuro Prognoz Meteorologicznych w Warszawie',
   'event': 'Orange Thunderstorm warning',
   'start': 1723982400,
   'end': 1724040000,
   'description': 'Thunderstorms are forecasted accompanied by the  precipitation amount 35 mm to 55 mm and wind gusts up to 90 km/h. Locally hail.',
   'tags': ['Thunderstorm']}]}
```

## Error handling

The API can return various HTTP status codes indicating errors:
- 400 Bad Request: Invalid request (e.g., missing required parameters).
- 401 Unauthorized: The most common reason is a missing, incorrect, or expired API key.
- 404 Not Found: Resources not found (e.g., invalid endpoint).
- 429 Too Many Requests: Exceeded the allowed number of API requests within a given time frame.
- 5xx Unexpected Error: Internal Server Error.

## Requirements and limitations

- **API key is required**: You can obtain your API key by signing up on the OpenWeather website. This key is used to authenticate your requests and must be included as a query parameter in every API call.
- **Query limits**: OpenWeather API has usage limits based on your subscription plan. Free tier users are typically subject to a limited number of requests per minute and per day. Exceeding these limits may result in your requests being temporarily blocked or returning error messages.

### Required Libraries

To run the code and perform data acquisition and processing, you need to install the following Python libraries:

1. **requests**: To perform HTTP GET requests.
2. **pandas**: To handle CSV data and perform data manipulation.

You can install these libraries using pip if you haven’t already:
```bash
pip install requests pandas
```

### How to Run the Code
1. Save the code to a file, for example, openweather_api.py. 
2. Run the script using Python from your terminal or command prompt:

```bash
python openweather_api.py
```