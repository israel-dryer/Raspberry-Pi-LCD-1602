from newsapi import NewsApiClient
from RPLCD.i2c import CharLCD
from time import sleep
import pickle

#with open('news_api_key.txt','r') as f:
#    my_api_key = f.read()

#api = NewsApiClient(api_key=my_api_key)
# get headlines and save data to temp file for development
#data = api.get_top_headlines(category='business', country='us')
#with open('data.pkl','wb') as f:
#    pickle.dump(data, f)

with open('data.pkl','rb') as f:
    data = pickle.load(f)

# options: get_everything(), get_sources(), get_top_headlines()

# extract specific items from the data pull
status = data.get('status') # confirms that the get-request was successful
total_results = data.get('totalResults') # the total number of results returned
articles = data.get('articles')
description = [row.get('description').replace(u'\xa0',' ') for row in articles] # remove non-breaking space (unicode)

def loop(desc):

    message = (desc[x:x+16] for x in range(0,len(desc),16))

    while True:
        try:
            # write message
            lcd.write_string(next(message))
            lcd.crlf()
            lcd.write_string(next(message))
            lcd.home()
            sleep(2)
            lcd.clear()
        except StopIteration:
            return

# create LCD
lcd = CharLCD(i2c_expander='PCF8574', address=0x27)

if __name__ == '__main__':
    lcd.clear()
    lcd.home()
    lcd.write_string('Loading...')
    lcd.home()
    lcd.clear()
    for d in description:
        loop(d)


