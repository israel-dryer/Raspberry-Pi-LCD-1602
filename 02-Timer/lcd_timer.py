######################################################################
#
#   Filename      : lcd_timer.py
#   Description   : End of the World Countdown Timer
#   Author        : Israel Dryer
#   Modified      : 2019-09-28
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
from math import floor

# current end of world prediction https://yourcountdown.to/the-end-of-the-world-2020
the_end = datetime(2020,1,1,23,59,59)

# calculate the number of seconds between the end and now
this_moment = datetime.now()
time_delta = the_end - this_moment
seconds = floor(time_delta.total_seconds())

def time_remains(sec):
    days = sec//86400
    hours = (sec//3600)%24
    minutes = (sec//60)%60
    secs = sec%60
    return '{}d {}h {}m {}s'.format(str(days).zfill(2),str(hours).zfill(2), str(minutes).zfill(2), str(secs).zfill(2))
    
def loop():
    global seconds
    while seconds > 0:
        # display message
        seconds -=1
        lcd.home()
        lcd.write_string('END OF THE WORLD\n\r')
        lcd.write_string(time_remains(seconds).rjust(16))
        sleep(1)
        
    lcd.message('The end has come!')    

# create LCD
lcd = CharLCD(i2c_expander='PCF8574', address=0x27)
lcd.clear()

if __name__ == '__main__':
    print('Program is starting...')
   
    try:
        loop()
    except:
        KeyboardInterrupt
        lcd.clear()
        lcd.close()