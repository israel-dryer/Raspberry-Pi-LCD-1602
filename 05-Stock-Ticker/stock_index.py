######################################################################
#   Filename      : stock_ticker.py
#   Description   : Display stock-index prices from yahoo finance 
#   Author        : Israel Dryer
#   Modified      : 2019-09-14
######################################################################
#
#   Install the required libraries
#   https://rplcd.readthedocs.io/en/stable/getting_started.html# 
#   sudo pip3 install RPLCD 
#   sudo pip3 install smbus
#
######################################################################
from RPLCD.i2c import CharLCD
from bs4 import BeautifulSoup
from time import sleep
import requests
import lxml

index = ['^GSPC', '^DJI', '^IXIC', '^RUT'] # S&P 500, DOW 30, NASDAQ, Russell 2000
url = 'https://finance.yahoo.com/quote/{}?p={}'

def get_html_data(index_list, url):
    # lookup index prices and save to dictionary
    html_data = {}
    for x in index:
        new_url = url.format(x, x)
        r = requests.get(new_url)
        html_data[x] = r.text    
    return html_data

def parse_html(html_data):
    # parse the html data and extract relevant parts for printing
    stock_ticker_data = []
    for stock, html in html_data.items():
        soup = BeautifulSoup(html, 'lxml')
        # current stock price
        price = soup.find('span',{'class':"Trsdu(0.3s)"})
        # change by amount and percent
        change_amt, change_pct = price.find_next_sibling().span.text.split(' ')
        # market close notice
        status, last_update = soup.find('div',{'id':'quote-market-notice'}).span.text.split(':  ')
        # save ticker data to list
        stock_ticker_data.append((stock, price.text.strip(), change_amt, change_pct, last_update))
    return stock_ticker_data

def formatter(data_row):
    # format the stock data and return 2 lines for printing to lcd
    stock, price, change_amt, change_pct, last_update = data_row
    line1 = stock
    line2 = '{} {}'.format(price, change_amt)
    return line1, line2
    
def loop():
    
    while True:
        # retrieve and parse stock-index prices
        html_data = get_html_data(index, url)
        stock_ticker_data = parse_html(html_data)

        # write message
        for stock in stock_ticker_data:
            line1, line2 = formatter(stock)

            lcd.home()
            lcd.clear()
            lcd.write_string(line1 + '\n\r')
            lcd.write_string(line2) 
            sleep(5)
        
# create LCD
lcd = CharLCD(i2c_expander='PCF8574', address=0x27)

if __name__ == '__main__':
    print('Program is starting...')
    lcd.clear()
    lcd.home()
    lcd.write_string('Loading...')
    
    try:
        loop()
    except:
        KeyboardInterrupt
        lcd.clear()
        lcd.close()