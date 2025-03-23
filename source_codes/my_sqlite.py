import sqlite3
import pandas as pd
import logging
import logging.config


def create_tables():
    """
    Create db and tables
    """
    logging.config.fileConfig("logging_config.ini")
    logger = logging.getLogger("db")

    try:
        conn = sqlite3.connect("stock_data.db", isolation_level=None)
        cursor = conn.cursor()

        sql = """create table if not exists stock_daily_price (
                    symbol varchar(10)
                    ,trade_date date
                    ,open float
                    ,high float
                    ,low float
                    ,close float
                    ,volume bigint )"""

        cursor.execute(sql)

    except sqlite3.Warning as warn:
        logger.warning(f"SQL Warning: {warn}")

    except sqlite3.Error as err:
        logger.error(f"SQL Error: {err}")

    finally:
        if conn:
            conn.close()


def insert_stock_price_data(stock_price_data):
    """
    Insert data to stock_daily_price
    """
    logging.config.fileConfig("logging_config.ini")
    logger = logging.getLogger("db")

    try:
        conn = sqlite3.connect("stock_data.db", isolation_level=None)
        cursor = conn.cursor()

        sql = "insert into stock_daily_price values (?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(sql, stock_price_data)

    except sqlite3.Warning as warn:
        logger.warning(f"SQL Warning: {warn}")

    except sqlite3.Error as err:
        logger.error(f"SQL Error: {err}")

    finally:
        if conn:
            conn.close()


def check_stock_price_table():
    """
    Sanity check for stock_daily_price, returns a dataframe
    """
    logging.config.fileConfig("logging_config.ini")
    logger = logging.getLogger("db")

    try:
        conn = sqlite3.connect("stock_data.db", isolation_level=None)
        cursor = conn.cursor()

        sql = "select symbol, count(*) as data_count, count(distinct trade_date) as date_count, min(trade_date) as min_trade_date, max(trade_date) as max_trade_date from stock_daily_price group by symbol order by symbol"
        df_result = pd.read_sql_query(sql, conn)
        return df_result

    except sqlite3.Warning as warn:
        logger.warning(f"SQL Warning: {warn}")

    except sqlite3.Error as err:
        logger.error(f"SQL Error: {err}")

    finally:
        if conn:
            conn.close()


def get_last_trade_date(symbol):
    """
    Get a symbol's last trade date in db
    """
    logging.config.fileConfig("logging_config.ini")
    logger = logging.getLogger("db")

    try:
        conn = sqlite3.connect("stock_data.db", isolation_level=None)
        cursor = conn.cursor()

        sql = "select max(trade_date) as last_trade_date from stock_daily_price where symbol = ?"
        cursor.execute(sql, (symbol,))
        last_trade_date = cursor.fetchone()[0]

        # if symbol not in db, return 1970-01-01 as last_trade_date
        if last_trade_date is None:
            last_trade_date = "1970-01-01"

        return last_trade_date

    except sqlite3.Warning as warn:
        logger.warning(f"SQL Warning: {warn}")

    except sqlite3.Error as err:
        logger.error(f"SQL Error: {err}")

    finally:
        if conn:
            conn.close()
