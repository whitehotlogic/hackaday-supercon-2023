import vga1_16x32 as font ## text 
import romans as deffont ## text
import gc9a01 ## text
from machine import Pin, SPI ## text
import math ## vector
import time ## vector
from vectorscope import Vectorscope ## vector

from screen import Screen # hack around vectorscope can only be reconstructed once per poweroff

def slideshow():
    
    """
    ## To animate, you need to clear v.wave.outBuffer_ready and wait for it to go true
    ## Each output buffer frame has 256 samples, so takes ~8.5 ms at 30 kHz

    #myscreen = Screen()
    #myscreen.init()

    v = Vectorscope()
    
    ramp = range(-2**15, 2**15, 2**8)
    
    v.wave.packX(ramp)
    
    v.wave.outBuffer_ready = False
    


    """
    spi = SPI(0, baudrate=40000000, sck=Pin(2, Pin.OUT), mosi=Pin(3, Pin.OUT), miso=Pin(20,Pin.IN))

    tft = gc9a01.GC9A01(spi, 240, 240,
        reset=Pin(4, Pin.OUT),
        cs=Pin(26, Pin.OUT),  
        dc=Pin(5, Pin.OUT),
        backlight=Pin(27, Pin.OUT),  
        rotation=0)
            
    tft.init()
    
    foreground = gc9a01.color565(10,15,10)
    background = gc9a01.color565(45, 217, 80)

    while(True):
        

        tft.fill(background)
        utime.sleep(1)

        height = tft.height()
        width = tft.width()
        last_line = height - font.HEIGHT

        tfa = 0        # top free area
        tfb = 0        # bottom free area
        tft.vscrdef(tfa, height, tfb)

        scroll = 0
        character = font.FIRST

        while True:
            # clear top line before scrolling off display
            tft.fill_rect(0, scroll, width, 1, background)

            # Write new line when we have scrolled the height of a character
            if scroll % font.HEIGHT == 0:
                line = (scroll + last_line) % height

                # write character hex value as a string
                tft.text(
                    font,
                    'x{:02x}'.format(character),
                    16,
                    line,
                    foreground,
                    background)

                # write character using a integer (could be > 0x7f)
                tft.text(
                    font,
                    character,
                    90,
                    line,
                    foreground,
                    background)

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


        """
        ## -------------
        ## slide 1: text
        ## -------------

        ## clear green
        tft.fill_rect(0,0,240,240,gc9a01.color565(45, 217, 80))

        tft.text(font,'hello world',20,120,
                 gc9a01.color565(10,15,10), ## foreground color
                 gc9a01.color565(45, 217, 80)) ## background color

        time.sleep(2)

        ## -------------
        ## slide 2: text
        ## -------------

        ## clear green
        tft.fill_rect(0,0,240,240,gc9a01.color565(45, 217, 80))

        tft.text(font,'hello gnarlsmarley',20,120,
                 gc9a01.color565(10,15,10), ## foreground color
                 gc9a01.color565(45, 217, 80)) ## background color

        time.sleep(2)
        
        ## clear black
        tft.fill_rect(0,0,240,240,gc9a01.color565(10,15,10))
        
        ## -------------
        ## slide 3: text
        ## -------------

        ## clear green
        tft.fill_rect(0,0,240,240,gc9a01.color565(45, 217, 80))

        ## tft.draw will accept scale, but not bgcolor

        tft.text(font,'hello swedishhat',20,120,
                 gc9a01.color565(10,15,10), ## foreground color
                 gc9a01.color565(45, 217, 80)) ## background color

        time.sleep(2)
        
        ## clear black
        tft.fill_rect(0,0,240,240,gc9a01.color565(10,15,10))
        
        ## -------------
        ## slide 4: text
        ## -------------

        ## clear green
        tft.fill_rect(0,0,240,240,gc9a01.color565(45, 217, 80))

        ## tft.draw will accept scale, but not bgcolor

        tft.text(font,'hello di0',20,120,
                 gc9a01.color565(10,15,10), ## foreground color
                 gc9a01.color565(45, 217, 80)) ## background color

        time.sleep(2)
        """
        
        ## ---------------
        ## slide 1: vector
        ## ---------------

        ## clear black
        #tft.fill_rect(0,0,240,240,gc9a01.color565(10,15,10))
        #time.sleep(2)
        
        for i in range(50):
            
            sine = [int(math.sin((50*i)+2*x*math.pi/256)*16_000) for x in range(256)]
            
            while not v.wave.outBuffer_ready:
                pass
            
            #time.sleep(0.015)
            
            v.wave.packY(sine)
            
            v.wave.outBuffer_ready = False
        
        #for i in range(100):
        #    v.deinit()
        
        ##v = None
        
        ## -------------
        ## slide 1: text
        ## -------------
        
        time.sleep(2)

        ## clear green
        v.screen.tft.fill_rect(0,0,240,240,gc9a01.color565(45, 217, 80))

        v.screen.tft.text(font,'hello world',20,120,
                 gc9a01.color565(10,15,10), ## foreground color
                 gc9a01.color565(45, 217, 80)) ## background color

        time.sleep(2)
        


if __name__ == "__main__":

    ##v = Vectorscope()
    
    slideshow()
    
    ##v.deinit() ## if you don't do this you'll see `OSError: 16` in thonny output (must disconnect and reconnect the device)