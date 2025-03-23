import os
import sys
import logging
import logging.config
import configparser
import requests
import pandas as pd
import my_classes
import my_sqlite as sql


def main():
 
    # make folder "logs" if not exists
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # start logger
    logging.config.fileConfig("logging_config.ini")
    logger = logging.getLogger("main")
    logger.info("Program started")

    # create stock_data.db and tables if not exists
    sql.create_tables()

    # read settings.ini, get settings to create url
    settings_file = "settings.ini"
    section = "Daily Stock Price Data Settings"
    config = configparser.ConfigParser()

    try:
        config.read(settings_file)
        settings = dict(config.items(section))
    except FileNotFoundError:
        logger.error(f"FileNotFound Error: {settings_file} not found.")
        logger.info("Program failed!\n\n")
        sys.exit()
    except configparser.Error as err:
        logger.error(f"ConfigParser Error: {err}")
        logger.info("Program failed!\n\n")
        sys.exit()
    except Exception as errex:
        logger.error(f"Exception: {errex}")
        logger.info("Program failed!\n\n")
        sys.exit()

    url = settings['url']
    data_type = settings['data_type']
    api_key = settings['api_key']
    data_tag = settings['data_tag']

    try:
        stocks = pd.read_csv('stock_list.txt', sep=",", header=None)[0].tolist()
    except FileNotFoundError:
        logger.error(f"FileNotFound Error: stock_list.txt not found.")
        logger.info("Program failed!\n\n")
        sys.exit()
    except pd.errors as err:
        logger.error(f"Dataframe Error: {err}")
        logger.info("Program failed!\n\n")
        sys.exit()
    except Exception as errex:
        logger.error(f"Exception: {errex}")
        logger.info("Program failed!\n\n")
        sys.exit()


    for i in range(len(stocks)):
        symbol = stocks[i]

        # if symbol not in db, get full history
        # otherwise, get last 100 trade dates data
        last_trade_date = sql.get_last_trade_date(symbol)
        if last_trade_date == "1970-01-01":
            output_size = "full"
        else:
            output_size = "compact"

        api_url = url + 'query?function=' + data_type + '&symbol=' + symbol + '&outputsize=' + output_size + '&apikey=' + api_key

        try: 
            response = requests.get(api_url)
            response.raise_for_status() 

            data = response.json()
            price_data = data[data_tag]
        except requests.exceptions.RequestException as errex:
            logger.error(f"API Exception - {symbol}: {errex}")
            continue
        except KeyError as kerr:
            logger.error(f"Key Error - {symbol}: {kerr}")
            continue
        else:
            logger.info(f"Download and parse successfully: {symbol}")


        for trade_date in price_data:
            # insert full history on first download
            # insert new data on subsequent downloads
            if trade_date > last_trade_date:
                stock = my_classes.Stock(symbol, trade_date, price_data[trade_date])
                prices = (stock.symbol, stock.trade_date, stock.open, stock.high, stock.low, stock.close, stock.volume)
                sql.insert_stock_price_data(prices)

    # sanity check for stock_daily_price, log output dataframe
    df_result = sql.check_stock_price_table()
    logger.info(f"DB data check:\n{df_result}")

    logger.info("Program done!\n")


if __name__ == "__main__":
    main()
