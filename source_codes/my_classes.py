import re

class Stock:
    """
    Stock has symbol, trade date, and price attributes vary based on the input price dictionary
    """
      
    def __init__(self, symbol, date, price_dict):
        """Constructor"""

        setattr(self, 'symbol', symbol)
        setattr(self, 'trade_date', date)

        # example of key for price dict: '1. open'
        # remove '1. ', mod the key to 'open', and open becomes an attribute of Stock object
        # also remove all special characters
        for tag in price_dict:
            tag_mod = re.sub(r'[^a-zA-Z]', '', tag)
            setattr(self, tag_mod, price_dict[tag])
