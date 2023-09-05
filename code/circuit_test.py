import utime
from IoHandler import IoHandler
import random

# run the top 4 neopixel scrolling loop
def neopixels():
    led_colour = 0
    while True:
        new_colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        for pixel in range(IoHandler.rgb_leds_count):
            IoHandler.set_rgb_pixel(pixel, new_colour)
        IoHandler.show_rgb_leds()

        # cycle leds
        led_colour += 1
        led_colour = led_colour % 3
        IoHandler.clear_led('red')
        IoHandler.clear_led('green')
        IoHandler.clear_led('yellow')
        if led_colour == 0:
                IoHandler.set_led('red')
        elif led_colour == 1:
                IoHandler.set_led('green')
        elif led_colour == 2:
                IoHandler.set_led('yellow')

        # test buttons
        if IoHandler.button_down('menu'):
            print('menu')
        if IoHandler.button_down('up'):
            print('up')
        if IoHandler.button_down('down'):
            print('down')
        if IoHandler.button_down('left'):
            print('left')
        if IoHandler.button_down('right'):
            print('right')
        if IoHandler.button_down('ok'):
            print('ok')

        utime.sleep(1)

neopixels()