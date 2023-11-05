### https://raw.githubusercontent.com/russhughes/gc9a01_mpy/main/examples/RP2/scroll.py
"""
scroll.py

    Smoothly scroll all characters of a font up a
    GC9A01 display connected to a Raspberry Pi Pico.

    Pico Pin   Display
    =========  =======
    14 (GP10)  BL
    15 (GP11)  RST
    16 (GP12)  DC
    17 (GP13)  CS
    18 (GND)   GND
    19 (GP14)  CLK
    20 (GP15)  DIN

    Fonts heights must be even multiples of the screen height
    (i.e. 8 or 16 pixels high).

"""
import utime
from machine import Pin, SPI
import gc9a01

import vga1_16x32 as font


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


def main():
    
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

    tft.init()
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
                #'x{:02x}'.format(character),
                'hackaday 2023',
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


main()
