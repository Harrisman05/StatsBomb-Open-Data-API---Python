# StatsBomb-Open-Data-API---Python

## View Champions League Final lineups + goalscorers in the terminal

An API built using Python's requests library to pull raw data from StatsBomb free data resources (https://github.com/statsbomb/open-data) and generate football formations and results in the terminal. The raw JSON data is manipulated in Python in order to be presented in a readable format in the terminal.

## How to install and run project

* Clone this repository
* Simply run statsbomb.py (have Python installed)

## How it works

* A GET request is sent to the StatsBomb open data endpoint to retrieve the raw data, which is then converted to JSON

<p align="center">
  <img src="https://github.com/Harrisman05/StatsBomb-Open-Data-API---Python/blob/master/assets/get_request_demo.png" width="60%" height="60%"/>
</p>

* JSON data is manipulated in Python code and then relevant data is printed to console

<p align="center">
  <img src="https://github.com/Harrisman05/StatsBomb-Open-Data-API---Python/blob/master/assets/print_statements_demo.png" width="50%" height="50%"/>
</p>

* Below is an example of outputted data:

<p align="center">
  <img src="https://github.com/Harrisman05/StatsBomb-Open-Data-API---Python/blob/master/assets/terminal_output.png" width="40%" height="40%"/>
</p>
