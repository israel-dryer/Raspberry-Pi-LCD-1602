from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
from ship_char import *
from random import randint
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
lcd = CharLCD(i2c_expander='PCF8574',address=0x27)
lcd.cursor_pos=(0,1)
lcd.clear()
vpos = 0
start = time.time()
speed = 1

def ship_up(char, boss, change):
    global div, lcd, vpos, start
    vpos += change
    mpos = max([0, 13-int(((time.time()-start)//speed))])
    lcd.create_char(0, char[vpos][0])
    lcd.create_char(1, char[vpos][1])
    lcd.create_char(4, boss[randint(0,2)])    
    lcd.cursor_pos=(0,1)
    string = f'\x00\n\r \x01{" "*mpos}\x04{" "*(13-mpos)}'
    lcd.write_string(string)

def ship_dwn(char, boss, change):
    global div, lcd, vpos, start
    vpos += change
    mpos = max([0, 13-int(((time.time()-start)//speed))])
    lcd.create_char(2, char[vpos][0])
    lcd.create_char(3, char[vpos][1])
    lcd.create_char(4, boss[randint(0,2)])
    lcd.cursor_pos=(0,1)
    string = f'\x02\n\r \x03{" "*mpos}\x04{" "*(13-mpos)}'
    lcd.write_string(string)

while True:
    input_state = GPIO.input(18)
    if input_state == False:
        if vpos > 0:
            ship_up(shipchar, meteorite, -1)
            time.sleep(0.01)
        else:
            ship_up(shipchar, meteorite, 0)
            time.sleep(0.01)
    else:
        if vpos < 8:
            ship_dwn(shipchar, meteorite, 1)
            time.sleep(0.01)
        else:
            ship_dwn(shipchar, meteorite, 0)
            time.sleep(0.01)
