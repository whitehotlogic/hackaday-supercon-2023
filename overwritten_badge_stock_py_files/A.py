'''
toasters.py

    [forked: https://github.com/russhughes/gc9a01_mpy/tree/main]

    [forked: spritesheet from CircuitPython_Flying_Toasters
    https://learn.adafruit.com/circuitpython-sprite-animation-pendant-mario-clouds-flying-toasters]

    [dependencies: t1.py, t2.py, t3.py, t4.py, t5.py]

    An example using bitmap to draw sprites on a GC9A01 display connected
    to a Raspberry Pi Pico.

    Pico Pin   Display
    =========  =======
    14 (GP10)  BL
    15 (GP11)  RST
    16 (GP12)  DC
    17 (GP13)  CS
    18 (GND)   GND
    19 (GP14)  CLK
    20 (GP15)  DIN
'''

import time
import random
from machine import Pin, SPI
import gc9a01
import t1, t2, t3, t4, t5

TOASTERS = [t1, t2, t3, t4]
TOAST = [t5]


class toast():
    '''
    toast class to keep track of a sprites location and step
    '''
    def __init__(self, sprites, x, y):
        self.sprites = sprites
        self.steps = len(sprites)
        self.x = x
        self.y = y
        self.step = random.randint(0, self.steps-1)
        self.speed = random.randint(2, 5)

    def move(self):
        if self.x <= 0:
            self.speed = random.randint(2, 5)
            self.x = 240-64

        self.step += 1
        self.step %= self.steps
        self.x -= self.speed


def main():
    '''
    Draw and move sprite
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

    # create toast spites in random positions
    sprites = [
        toast(TOASTERS, tft.width()-64, 0),
        toast(TOAST, tft.width()-64*2, 80),
        toast(TOASTERS, tft.width()-64*4, 160)
    ]

    # move and draw sprites
    while True:
        for man in sprites:
            bitmap = man.sprites[man.step]
            tft.fill_rect(
                man.x+bitmap.WIDTH-man.speed,
                man.y,
                man.speed,
                bitmap.HEIGHT,
                gc9a01.BLACK)

            man.move()

            if man.x > 0:
                tft.bitmap(bitmap, man.x, man.y)
            else:
                tft.fill_rect(
                    0,
                    man.y,
                    bitmap.WIDTH,
                    bitmap.HEIGHT,
                    gc9a01.BLACK)

        time.sleep(0.05)


main()




### original badge code for this file -- di0
"""
from vectorscope import Vectorscope
import vectoros
import keyboardcb
import keyleds
import asyncio

import random_walk 

_abort=False

async def random_walker(v):
    ## Minimal example
    global _abort
    r = random_walk.RW(v)
    x,y = 0,0
    while _abort==False:
        x,y = r.random_walk(x,y)
        ## this is important -- it yields to the key scanner
        await asyncio.sleep_ms(10)
            
## Below here is boilerplate.  
def do_abort(key):
    global _abort
    _abort=True
    
from vos_state import vos_state

async def slot_main(v):
    global _abort
    # watch the keys -- you can define your own callbacks here
    mykeys = keyboardcb.KeyboardCB( {keyleds.KEY_MENU: do_abort} )
    await random_walker(v)
    print("OK done")
"""