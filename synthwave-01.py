### https://thepihut.com/blogs/raspberry-pi-tutorials/coding-graphics-with-micropython-on-raspberry-pi-pico-displays

from machine import Pin,SPI,PWM
import machine
import framebuf
import utime
import gc
import gc9a01

spi = SPI(0, baudrate=40000000, sck=Pin(2, Pin.OUT), mosi=Pin(3, Pin.OUT), miso=Pin(20,Pin.IN))

tft = gc9a01.GC9A01(spi, 240, 240,
    reset=Pin(4, Pin.OUT),
    cs=Pin(26, Pin.OUT),  
    dc=Pin(5, Pin.OUT),
    backlight=Pin(27, Pin.OUT),  
    rotation=0)

#tft.init()
tft.fill(gc9a01.BLACK)

#for x in range(250):
#    tft.pixel(x, x*2, gc9a01.RED)
    
    
# THING1: draws thing forwards, right
for i in range(0,122,8):
    tft.line(0,20+i,i,140,gc9a01.YELLOW)
    utime.sleep(0.05)
 
# cls
tft.fill(gc9a01.BLACK)

# THING1: draws thing backwards, left
for i in range(122,0,-8):
    tft.line(0,20+i,i,140,gc9a01.YELLOW)
    utime.sleep(0.05)
    
# THING1: draws thing inverted downwards, left (NOT AS INTENDED, BUT STILL COOL)
for i in range(300,122,-8):
    tft.line(0,20+i,i,140,gc9a01.YELLOW)
    utime.sleep(0.05)
    
# THING1: draws thing mirrored downwards, from upper left
for i in range(240,0,-8):
    tft.line(i,240,20+i,140,gc9a01.YELLOW)
    utime.sleep(0.05)

#for i in range(0,400,4):
#    tft.line(0,50+i,i,150,gc9a01.YELLOW)
#    utime.sleep(0.05)
    
#for i in range(10,100,4):
#    tft.line(400,i-50,i-50,150,gc9a01.YELLOW)

#for i in range(4,281,0):
#    tft.line(0,50-i,i,200,gc9a01.YELLOW)
#    utime.sleep(0.1)

##tft.show()
