import utime
from IoHandler import IoHandler
import random

# run the top 4 neopixel scrolling loop
def neopixels():
    led_colour = 0
    loop_counter = 0

    last_colour = (0, 0, 0)
    new_colour = (random.randint(0, 64), random.randint(0, 64), random.randint(0, 64))
    fade_in_out = 1

    while True:

        if loop_counter == 50:
            last_colour = new_colour
            if fade_in_out == 1: # fade in finished
                new_colour = (0, 0, 0)
                fade_in_out = 0
            else: # fade out finished
                new_colour = (random.randint(0, 64), random.randint(0, 64), random.randint(0, 64))
                fade_in_out = 1

            loop_counter = 0


        red = (int)(last_colour[0] + ((new_colour[0] - last_colour[0]) * loop_counter / 50))
        green = (int)(last_colour[1] + ((new_colour[1] - last_colour[1]) * loop_counter / 50))
        blue = (int)(last_colour[2] + ((new_colour[2] - last_colour[2]) * loop_counter / 50))
        current_colour = (red, green, blue)

        for pixel in range(IoHandler.rgb_leds_count):
            IoHandler.set_rgb_pixel(pixel, current_colour)
        IoHandler.show_rgb_leds()

        loop_counter += 1

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

        utime.sleep(0.1)

neopixels()