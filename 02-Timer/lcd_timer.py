######################################################################
#
#   Filename      : lcd_timer.py
#   Description   : End of the World Countdown Timer
#                   https://en.wikipedia.org/wiki/List_of_dates_predicted_for_apocalyptic_events
#   Author        : Israel Dryer
#   Modified      : 2020-03-04
#
######################################################################
#
#   Install the required libraries
#   https://rplcd.readthedocs.io/en/stable/getting_started.html# 
#   sudo pip3 install RPLCD 
#   sudo pip3 install smbus
#
######################################################################
from RPLCD.i2c import CharLCD
from time import sleep
from datetime import datetime


def num2str(num):
    """ Convert floating value to integer-like string """
    return str(int(num)).zfill(2)


def time_remains(end_datetime):
    """ Calculate time remaining between now and predicted end of world """
    this_moment = datetime.now()
    
    # calculate components of remaining time from datetime object
    seconds = (end_datetime - this_moment).total_seconds()
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    mins, seconds = divmod(seconds, 60)
    
    # create a return the formatted string
    return "{}d {}h {}m {}s".format(num2str(days), num2str(hours), num2str(mins), num2str(seconds))
    
    
def loop(end_datetime):
    """ Main program loop """
    while True:
        lcd_msg = time_remains(end_datetime)
        lcd.home()
        
        if lcd_msg:
            lcd.write_string("END OF THE WORLD\n\r")
            lcd.write_string(lcd_msg.rjust(16))
            sleep(1)
            
        else: # an empty string will end the program
            lcd.write_string("THE END HAS COME!")
            break
    return


if __name__ == '__main__':
    print('Program is starting...')
   
    # set timer end datetime
    the_end = datetime(2020,12,31,23,59,59)
    
    # create LCD object
    lcd = CharLCD(i2c_expander='PCF8574', address=0x27)
    lcd.clear()

    try:
        loop(the_end)
    except:
        KeyboardInterrupt # CTRL+C
        lcd.clear()
        lcd.close()