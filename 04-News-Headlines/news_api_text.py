from newsapi import NewsApiClient
from RPLCD.i2c import CharLCD
from time import sleep
import pickle

with open('news_api_key.txt','r') as f:
    my_api_key = f.read()
api = NewsApiClient(api_key=my_api_key)
data = api.get_top_headlines(category='technology', country='us', page_size=100)    

def parse_data(data):
    '''parse the lines in each article into a list of lcd rows, where each row
       is limited to a max of 16 characters and there are no breaks in words'''
    letter_cnt = 0 # a running count of characters for each line
    word_list = [] # a cumulative list of words for each line
    lcd_line_list = [] # a cumulative list word_lists for each article
    for word in data:
        # a line on the lcd display cannot exceed 16 characters
        if letter_cnt + len(word) + len(word_list) < 17:
            word_list.append(word)
            letter_cnt += len(word)
        else:
            # if the running character count exceeds 16 characters, add the cumulative list
            # of words as a line in the lcd_line_list and restart the process from the
            # current position
            letter_cnt = len(word)+1
            lcd_line_list.append(word_list.copy())
            word_list.clear()
            word_list.append(word)
    # there will be a final set of words remaining in each article that are appended to the word list
    if len(word_list) > 0:
        lcd_line_list.append(word_list.copy())
    return lcd_line_list

def build_lines(data):
    ''' build a list of articles that have been parsed and ready to display on the 16x2 lcd display'''
    # retrieve the article data from the request item returned from NewsApi
    article_data = data.get('articles')
    # split the words of each article into a list.. removing non-breaking spaces '\xa0'
    articles = [article.get('description').replace(u'\xa0',' ').split(' ') for article in article_data if article.get('description') is not None]
    titles = [title.get('title').replace(u'\xa0',' ').split(' ') for title in article_data if title.get('description') is not None]
    # parse each article to fit the requirements of a 16x2 display
    article_list = [parse_data(article) for article in articles]
    title_list = [parse_data(title) for title in titles]
    return iter(article_list), iter(title_list)

def reset_lcd():
    '''return the cursor to home position and clear'''
    lcd.home()
    lcd.clear

def loop():
    title_raw = next(title_lines)
    title = (' '.join(row) for row in title_raw)
    message_raw = next(article_lines)
    message = (' '.join(row) for row in message_raw)

    def show_title():
        while True:
            try:
                # write message
                lcd.write_string(next(title))
                lcd.crlf()
                lcd.write_string(next(title))
                lcd.home()
                sleep(2)
                lcd.clear()
            except StopIteration:
#                reset_lcd()
#                lcd.write_string('-'*16)
#                sleep(1)
#                reset_lcd()
                return
#    def show_article():
#        while True:
#            try:
#                # write message
#                lcd.write_string(next(message))
#                lcd.crlf()
#                lcd.write_string(next(message))
#                lcd.home()
#                sleep(2)
#                lcd.clear()
#            except StopIteration:
#                return
    show_title()
#    show_article()
    return

article_lines, title_lines = build_lines(data)

# create LCD
lcd = CharLCD(i2c_expander='PCF8574', address=0x27)


if __name__ == '__main__':
    # initiate the startup routine
    lcd.write_string('Loading...')

    # iterate through each article
    for i, lines in enumerate(article_lines):
        reset_lcd()
        lcd.write_string(f'ARTICLE {i+1:,d} --->')
        sleep(2)
        reset_lcd()
        loop()
        

