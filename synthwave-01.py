### https://thepihut.com/blogs/raspberry-pi-tutorials/coding-graphics-with-micropython-on-raspberry-pi-pico-displays

from machine import Pin,SPI,PWM
import machine
import framebuf
import utime
import gc
import gc9a01
import math


spi = SPI(0, baudrate=40000000, sck=Pin(2, Pin.OUT), mosi=Pin(3, Pin.OUT), miso=Pin(20,Pin.IN))

tft = gc9a01.GC9A01(spi, 240, 240,
    reset=Pin(4, Pin.OUT),
    cs=Pin(26, Pin.OUT),  
    dc=Pin(5, Pin.OUT),
    backlight=Pin(27, Pin.OUT),  
    rotation=0)

#tft.init()
tft.fill(gc9a01.BLACK)

def circle(x,y,r,c):
    tft.hline(x-r,y,r*2,c)
    for i in range(1,r):
        a = int(math.sqrt(r*r-i*i)) # Pythagoras!
        tft.hline(x-a,y+i,a*2,c) # Lower half
        tft.hline(x-a,y-i,a*2,c) # Upper half

# LEFT-MOUNTAIN: draws left, from bottom-to-top
for i in range(122,0,-8):
    tft.line(0,20+i,i,140,gc9a01.YELLOW)
    utime.sleep(0.05)
    
# TERRAIN: draws initial terrain lines, from bottom-to-top
for i in range(300,122,-8):
    tft.line(0,20+i,i,140,gc9a01.YELLOW)
    utime.sleep(0.05)
    
# TERRAIN: draws cross-grid terrain lines, from right-to-left
for i in range(240,0,-8):
    tft.line(i,240,20+i,140,gc9a01.YELLOW)
    utime.sleep(0.05)

# SKY: draws thing from right-to-left
for i in range(240,0,-8):
    tft.line(i,0,20+i,140,gc9a01.YELLOW)
    utime.sleep(0.05)
    
circle(160,100,30,gc9a01.YELLOW)

#for x in range(250):
#    tft.pixel(x, x*2, gc9a01.RED)

#
#
#   lcd.line(x1, y1, x2, y2, color)
#    
#

#circle(120,120,50,gc9a01.YELLOW)

"""
utime.sleep(2)


# RIGHT-MOUNTAIN?
for i in range(0,122,8):
    tft.line(i,140,244,20+i,gc9a01.YELLOW)
    utime.sleep(0.05)

utime.sleep(2)

# RIGHT-MOUNTAIN: works upside down
for i in range(122,244,8):
    tft.line(i,140,244,20+i,gc9a01.YELLOW)
    utime.sleep(0.05)
    
# LEFT-MOUNTAIN: draws right, from top-to-bottom
for i in range(0,122,8):
    tft.line(0,20+i,i,140,gc9a01.YELLOW)
    utime.sleep(0.05)
"""

# cls
#tft.fill(gc9a01.BLACK)


    
# RIGHT-MOUNTAIN: cool but no 
#for i in range(122,0,-8):
#    tft.line(i,140,244,20-i,gc9a01.YELLOW)
#    utime.sleep(0.05)



# MAYBE USEFUL CENTERED GODRAY THING
#for i in range(240,0,-8):
#    tft.line(122,122,20+i,240,gc9a01.YELLOW)
#    utime.sleep(0.05)

#for i in range(0,400,4):
#    tft.line(0,50+i,i,150,gc9a01.YELLOW)
#    utime.sleep(0.05)
    
#for i in range(10,100,4):
#    tft.line(400,i-50,i-50,150,gc9a01.YELLOW)

#for i in range(4,281,0):
#    tft.line(0,50-i,i,200,gc9a01.YELLOW)
#    utime.sleep(0.1)

##tft.show()
