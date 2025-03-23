import configparser

def create_config(path):
    """
    Create a config file
    """

    config = configparser.ConfigParser()

    url = "https://www.alphavantage.co/"
    api_key = "XSPICKDC3ZLQ1DB9"

    config.add_section("Daily Stock Price Data Settings")
    config.set("Daily Stock Price Data Settings", "url", url)
    config.set("Daily Stock Price Data Settings", "api_key", api_key)
    config.set("Daily Stock Price Data Settings", "data_type", "TIME_SERIES_DAILY")
    config.set("Daily Stock Price Data Settings", "data_tag", "Time Series (Daily)")


    config.add_section("Adj Daily Stock Price Data Settings")
    config.set("Adj Daily Stock Price Data Settings", "url", url)
    config.set("Adj Daily Stock Price Data Settings", "api_key", api_key)
    config.set("Adj Daily Stock Price Data Settings", "data_type", "TIME_SERIES_DAILY_ADJUSTED")
    config.set("Adj Daily Stock Price Data Settings", "data_tag", "Time Series (Daily)")

    with open(path, "w") as config_file:
        config.write(config_file)


if __name__ == "__main__":
    create_config("settings.ini")
