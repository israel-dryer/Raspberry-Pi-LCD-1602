#!/usr/bin/env python3
########################################################################
# Filename    : lcd_timer.py
# Description : LCD Display Timer
# Author      : Israel Dryer
# modification: 2019/09/12 
########################################################################
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
from time import sleep

def time_remains(sec):
    hours = sec//(60*60)
    minutes = (sec//60%60)
    secs = sec%60
    return '{}:{}:{}'.format(str(hours).zfill(2), str(minutes).zfill(2), str(secs).zfill(2))

def loop():
    global seconds
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns

    while seconds > 0:
        # display message
        seconds -=1
        lcd.setCursor(0,0)  # set cursor position
        lcd.message('    Pi Timer\n') # 1st line header
        lcd.message('    ' + time_remains(seconds)) # 2nd line timer
        sleep(1)
        
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
    mins = int(input("How many minutes? "))
    seconds = mins * 60
   
    try:
        loop()
    except KeyboardInterrupt:
        destroy()