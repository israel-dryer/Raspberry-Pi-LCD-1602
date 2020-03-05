######################################################################
#
#   Filename      : stock_ticker.py
#   Description   : Display stock/index prices from yahoo finance
#   Author        : Israel Dryer
#   Modified      : 2020-03-04
#
######################################################################
#
#   Install the required libraries
#   https://rplcd.readthedocs.io/en/stable/getting_started.html#
#   sudo pip3 install RPLCD
#   sudo pip3 install smbus
#   sudo pip3 install bs4
#   sudo pip3 install lxml
#   sudo pip3 install requests
#
######################################################################
from RPLCD.i2c import CharLCD
from bs4 import BeautifulSoup
from time import sleep
import requests
import lxml

# add to this list or replace with any stock/index you want on Yahoo! Finance
index = {'^GSPC':'S&P 500', '^DJI':'DOW 30', '^IXIC':'NASDAQ', '^RUT':'Russell 2000'} 
url = 'https://finance.yahoo.com/quote/{}?p={}'

def get_curr_prices(index_list, url):
    """ Create a dictionary containing current index prices """
    
    curr_prices = {}
    
    for symbol, name in index.items():
        
        # create url with index symbol
        new_url = url.format(symbol, symbol)
        
        # get the index html data from yahoo finance
        r = requests.get(new_url)
        
        # save name and price information in dictionary: {name: price}
        curr_prices[name] = r.text
        
    return curr_prices


def parse_html(html_data):
    """ Parse html data and extract relevant sections """
    
    ticker_data = []
    
    for stock, html in html_data.items():
        
        # create BS4 object for parsing html
        soup = BeautifulSoup(html, 'lxml')
        
        # current index price
        price = soup.find('span',{'class':"Trsdu(0.3s)"})
        
        # change by amount and percent
        change_amt, change_pct = price.find_next_sibling().span.text.split(' ')
        
        # market close notice
        status, last_update = soup.find('div',{'id':'quote-market-notice'}).span.text.split(':  ')
        
        # save ticker data to list
        ticker_data.append((stock, price.text.strip(), change_amt, change_pct, last_update))
        
    return ticker_data



def formatter(data_row):
    """ format the stock data and return 2 lines for printing to lcd """
    stock, price, change_amt, change_pct, last_update = data_row
    line1 = stock
    line2 = '{} {}'.format(price, change_amt)
    return line1, line2


def loop():
    """ The main program loop """
    while True:
        
        # retrieve and parse stock-index prices
        curr_prices = get_curr_prices(index, url)
        ticker_data = parse_html(curr_prices)

        # write message
        for item in ticker_data:
            line1, line2 = formatter(item)

            lcd.home()
            lcd.clear()
            lcd.write_string(line1 + '\n\r')
            lcd.write_string(line2)
            sleep(5)  # delay for 5 seconds between indexes


if __name__ == '__main__':

    # Initialize LCD object
    lcd = CharLCD(i2c_expander='PCF8574', address=0x27)
    lcd.clear()
    lcd.home()
    lcd.write_string('Loading...')

    try:
        loop()
    except:
        KeyboardInterrupt  # CTRL+C
        lcd.clear()
        lcd.close()