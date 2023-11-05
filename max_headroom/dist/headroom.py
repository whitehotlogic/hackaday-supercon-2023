'''
headroom.py
'''

import time
import random
from machine import Pin, SPI
import gc9a01
import h1, h2, h3#, h4, h5#, h11, h12, h13, h14, h15 

FRAMES = [h1, h2, h3]#, h4, h5]#, h11, h12, h13, h14, h15]

def main():
    '''
    Animate FRAMES
    '''

    spi = SPI(0, baudrate=40000000, sck=Pin(2, Pin.OUT), mosi=Pin(3, Pin.OUT), miso=Pin(20,Pin.IN))
    
    tft = gc9a01.GC9A01(spi, 240, 240,
        reset=Pin(4, Pin.OUT),
        cs=Pin(26, Pin.OUT),  
        dc=Pin(5, Pin.OUT),
        backlight=Pin(27, Pin.OUT),  
        rotation=0)

    # enable display and clear screen
    tft.init()
    tft.fill(gc9a01.BLACK)

    while True:
        for frame in FRAMES:
            tft.bitmap(frame, 0, 20)
            time.sleep(0.05)    

main()
