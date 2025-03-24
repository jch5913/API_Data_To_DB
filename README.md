Description

The purpose of the program is to pull stock daily data from AlphaVantage's API, store to an SQLite database.


Features

•	Users can specify the stocks of interest in the stock_list.txt file.

•	Data are stored in stock_data.db, table is stock_daily_price.

•	On the first download of a stock, the program gets and loads to database the full history of the stock. On subsequent runs, only new data are inserted to the database.

Installation

To run this program, an API key from AlphaVantage is needed (https://www.alphavantage.co/support/#api-key). The free API key gives access to non-premium APIs only, and limits to 25 API requests per day. Save API key in settings.ini, under api_key.

To run the program, download the source_codes folder. For reference, I use Python 3.13.
