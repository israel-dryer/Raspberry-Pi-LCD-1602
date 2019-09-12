##############################################################################
###
#   Filename    :   stock_index.py
#   Author      :   Israel Dryer
#   Written     :   2019-09-12
#   Purpose     :   Extract stock-index prices from yahoo finance and update
###                 an LCD display attached to the Raspberry Pi
####
##############################################################################
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
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
    line1 = stock + ' : ' + last_update 
    line2 = '{} {} {}'.format(price, change_amt, change_pct)
    return line1, line2


def loop():
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns

    while True:
        # retrieve and parse stock-index prices
        html_data = get_html_data(index, url)
        stock_ticker_data = parse_html(html_data)
        
        for stock in stock_ticker_data:
            line1, line2 = formatter(stock)

            # display message
            seconds -=1
            lcd.setCursor(0,0)  # set cursor position
            lcd.message(line1 + '\n')
            lcd.message(line2) 
            sleep(5)
        
    lcd.message('Time is Up!')

def destroy():
    lcd.clear()

PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
	mcp = PCF8574_GPIO(PCF8574_address)
except:
	try:
		mcp = PCF8574_GPIO(PCF8574A_address)
	except:
		print ('I2C Address Error !')
		exit(1)

# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

if __name__ == '__main__':
    print ('Program is starting ... ')
   
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

