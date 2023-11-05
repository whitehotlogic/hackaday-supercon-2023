import vga1_16x32 as font
import romans as deffont


import gc9a01
from machine import Pin, SPI

spi = SPI(0, baudrate=40000000, sck=Pin(2, Pin.OUT), mosi=Pin(3, Pin.OUT), miso=Pin(20,Pin.IN))

tft = gc9a01.GC9A01(spi, 240, 240,
    reset=Pin(4, Pin.OUT),
    cs=Pin(26, Pin.OUT),  
    dc=Pin(5, Pin.OUT),
    backlight=Pin(27, Pin.OUT),  
    rotation=0)
        
tft.init()

## clear
tft.fill_rect(0,0,240,240,gc9a01.color565(45, 217, 80))

## tft.draw will accept scale, but not bgcolor

tft.text(font,'hello world',20,120,
         gc9a01.color565(10,15,10), ## foreground color
         gc9a01.color565(45, 217, 80)) ## background color
