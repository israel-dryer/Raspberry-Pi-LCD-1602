######################################################################
#   Filename      : lcd_timer.py
#   Description   : LCD Display Timer 
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
from time import sleep

def time_remains(sec):
    hours = sec//(60*60)
    minutes = (sec//60%60)
    secs = sec%60
    return '{}:{}:{}'.format(str(hours).zfill(2), str(minutes).zfill(2), str(secs).zfill(2))
    
def loop():
    global seconds
    while seconds > 0:
        # display message
        seconds -=1
        lcd.home()
        lcd.write_string('    Pi Timer\n\r')
        lcd.write_string('    ' + time_remains(seconds))
        sleep(1)
        
    lcd.message('Time is Up!')    

# create LCD
lcd = CharLCD(i2c_expander='PCF8574', address=0x27)
lcd.clear()

if __name__ == '__main__':
    print('Program is starting...')
    mins = int(input('How many minutes? '))
    seconds = mins * 60
   
    try:
        loop()
    except:
        KeyboardInterrupt
        lcd.clear()
        lcd.close()