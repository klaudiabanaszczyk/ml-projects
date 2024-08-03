# Introduction

The data used in this project regarding actual values from the energy market are sourced from the official website of Polskie Sieci Elektroenergetyczne (PSE):
[https://www.pse.pl/home](https://www.pse.pl/home)

The website presents data on planned and current power flows in Poland, the demand and supplied power from various energy sources, as well as forecasted and settlement prices from the balancing market and additional services provided by PSE.

Data up to 14/06/2024 is retrieved using HTTP GET requests, which can be found in the `http` directory, while data from 14/06/2024 (inclusive) is retrieved from the PSE API, which can be found in the `api` directory.