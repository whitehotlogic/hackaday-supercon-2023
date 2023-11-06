'''
headroom.py
'''
import time
import utime
import random
from machine import Pin, SPI
import gc9a01
import vga1_16x32 as font
import h15, h6
import t1, t2, t3, t4, t5
import math

TOASTERS = [t1, t2, t3, t4]
TOAST = [t5]

FRAMES = [h15, h6]

# this one is worth keeping
#FRAMES = [h15, h16]

class toast():
    '''
    toast class to keep track of a sprites locaton and step
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


def toasters():
    
    spi = SPI(0, baudrate=40000000, sck=Pin(2, Pin.OUT), mosi=Pin(3, Pin.OUT), miso=Pin(20,Pin.IN))
    
    tft = gc9a01.GC9A01(spi, 240, 240,
        reset=Pin(4, Pin.OUT),
        cs=Pin(26, Pin.OUT),  
        dc=Pin(5, Pin.OUT),
        backlight=Pin(27, Pin.OUT),  
        rotation=0)

    # enable display and clear screen
    #tft.init()
    tft.fill(gc9a01.BLACK)

    # create toast spites in random positions
    sprites = [
        toast(TOASTERS, tft.width()-64, 0),
        toast(TOAST, tft.width()-64*2, 80),
        toast(TOASTERS, tft.width()-64*4, 160)
    ]

    # move and draw sprites
    #while True:
        
    for i in range(200):
    
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


def cycle(p):
    try:
        len(p)
    except TypeError:
        cache = []
        for i in p:
            yield i
            cache.append(i)
        p = cache
    while p:
        yield from p


def scrolltext():
    
    spi = SPI(0, baudrate=40000000, sck=Pin(2, Pin.OUT), mosi=Pin(3, Pin.OUT), miso=Pin(20,Pin.IN))
    
    tft = gc9a01.GC9A01(spi, 240, 240,
        reset=Pin(4, Pin.OUT),
        cs=Pin(26, Pin.OUT),  
        dc=Pin(5, Pin.OUT),
        backlight=Pin(27, Pin.OUT),  
        rotation=0)

    colors = cycle([0xe000, 0xece0, 0xe7e0, 0x5e0, 0x00d3, 0x7030])
    foreground = next(colors)
    background = gc9a01.BLACK

    #tft.init()
    tft.fill(background)
    #utime.sleep(1)

    height = tft.height()
    width = tft.width()
    last_line = height - font.HEIGHT

    tfa = 0        # top free area
    tfb = 0        # bottom free area
    tft.vscrdef(tfa, height, tfb)

    scroll = 0
    character = font.FIRST

    alternate = False

    #while True:
    for i in range(600):
        
        # clear top line before scrolling off display
        tft.fill_rect(0, scroll, width, 1, background)

        # Write new line when we have scrolled the height of a character
        if scroll % font.HEIGHT == 0:
            line = (scroll + last_line) % height

            if alternate:
                mytext = 'SUPERCON 2023'
                alternate = False
            else:
                mytext = 'Hackaday 2023'
                alternate = True

            # write character hex value as a string
            tft.text(
                font,
                #'x{:02x}'.format(character),
                #'hackaday 2023',
                mytext,
                16,
                line,
                foreground,
                background)

            """
            # write character using a integer (could be > 0x7f)
            tft.text(
                font,
                character,
                90,
                line,
                foreground,
                background)
            """

            # change color for next line
            foreground = next(colors)

            # next character with rollover at 256
            character += 1
            if character > font.LAST:
                character = font.FIRST

        # scroll the screen up 1 row
        tft.vscsad(scroll+tfa)
        scroll += 1
        scroll %= height

        utime.sleep(0.01)


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



    while True:
        
        tft.fill(gc9a01.BLACK)
        
        # enable display and clear screen
        tft.init()
        
        toasters()

        tft.fill(gc9a01.BLACK)
        
        for i in range(10):
            
            for frame in FRAMES:
                tft.bitmap(frame, 0, 0)
                time.sleep(0.05)    
          

        
        
        tft.fill(gc9a01.BLACK)
        tft.init()
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

        utime.sleep(2)

        ##### credits
        tft.fill(gc9a01.BLACK)
        
        scrolltext()

main()

"""
# list of things to launch from vectoros

# dictionary of tags to imports (will look for .vos_main() or .main() here) 
launch_list={ "menu": "supercon_menu", 'sketch': 'sketch', "demo": "examples", "planets":"planets", "lissajous":"lissajous"}

# list what you want to start auto (maybe just one thing?) need tag
auto_launch_list=["menu"]

vectorscope_slots={"slotA": "A", "slotB": "B", "slotC": "C", "slotD": "D"}

auto_launch_repl=False    # to get out: import sys followed by sys.exit()

key_scan_rate = 100    # how often to scan the keyboard globally (ms; 0 to do it yourself)

# how often to garbage collect
# if you set this to zero and do nothing else
# garbage collection will be automatic as usual and before new tasks launch
gc_thread_rate = 5000

# Base rate for the timer (ms)
timer_base_rate=100

# Debug level (messages must be < this level to print)
# That is, at level 0 only level 0 messages print
# at level 1 then level 1 and level 0 messages print
# Set level to -1 to stop all messages (assuming you only call debug_print with positive values)

# if you want to use symbols for debug level, these are defined in vos_debug:
DEBUG_LEVEL_SILENT=-1
DEBUG_LEVEL_SEVERE=0
DEBUG_LEVEL_ERROR=10
DEBUG_LEVEL_WARNING=20
DEBUG_LEVEL_INFO=30

debug_level=DEBUG_LEVEL_INFO


if __name__=="__main__":
    import vectoros
    vectoros.run()
"""