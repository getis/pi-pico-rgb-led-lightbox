# class to handle the IO for the demo setup
from machine import Pin
import neopixel

class IoHandler:
    # create array of neopixels
    rgb_leds_count = 256
    rgb_leds = neopixel.NeoPixel(Pin(0), rgb_leds_count)
    # create list of RGB tuples to control led states
    rgb_led_colours = [(0, 0, 0)] * rgb_leds_count

    # buttons
    btn_menu = Pin(22, Pin.IN, Pin.PULL_UP)
    btn_up = Pin(21, Pin.IN, Pin.PULL_UP)
    btn_left = Pin(20, Pin.IN, Pin.PULL_UP)
    btn_down = Pin(19, Pin.IN, Pin.PULL_UP)
    btn_right = Pin(18, Pin.IN, Pin.PULL_UP)
    btn_ok = Pin(17, Pin.IN, Pin.PULL_UP)


    # leds
    led_red = Pin(10, Pin.OUT)
    led_green = Pin(11, Pin.OUT)
    led_yellow = Pin(12, Pin.OUT)

    def __init__(self):
        # get everything into a starting state
        self.__class__.clear_rgb_leds()

    # output, setters and getters for coloured leds

    # rgb leds
    @classmethod
    def set_rgb_pixel(cls, pixel, colour):
        cls.rgb_leds[pixel] = colour
        cls.rgb_led_colours[pixel] = colour

    @classmethod
    def get_rgb_pixel(cls, pixel):
        return cls.rgb_led_colours[pixel]

    @classmethod
    def show_rgb_leds(cls):
        cls.rgb_leds.write()

    @classmethod
    def clear_rgb_leds(cls):
        for n in range(cls.rgb_leds_count):
            cls.set_rgb_pixel(n, (0, 0, 0))
        cls.show_rgb_leds()

    @classmethod
    def set_led(cls, colour):
        if colour == 'red':
            cls.led_red.on()
        elif colour == 'green':
            cls.led_green.on()
        elif colour == 'yellow':
            cls.led_yellow.on()

    @classmethod
    def clear_led(cls, colour):
        if colour == 'red':
            cls.led_red.off()
        elif colour == 'green':
            cls.led_green.off()
        elif colour == 'yellow':
            cls.led_yellow.off()

    @classmethod
    def button_down(cls, button):
        if button == 'menu':
            return cls.btn_menu.value() == 0
        elif button == 'up':
            return cls.btn_up.value() == 0
        elif button == 'down':
            return cls.btn_down.value() == 0
        elif button == 'left':
            return cls.btn_left.value() == 0
        elif button == 'right':
            return cls.btn_right.value() == 0
        elif button == 'ok':
            return cls.btn_ok.value() == 0

