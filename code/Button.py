# class to handle a single button

from machine import Pin

class Button:

    # constructor
    # pin  = IO pin number
    # state = 0 active low (pulled high), 1 active high (pulled low)
    def __init__(self, pin, active_state):
        self.active_state = active_state if active_state == 0 else 1
        if self.active_state:
            self.pin = Pin(pin, Pin.IN, Pin.PULL_DOWN)
        else:
            self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.state = (self.pin.value() == self.active_state)
        self.clicked = False

    def get_state(self):
        self.state = 1 if self.pin.value() == self.active_state else 0

    def scan(self):
        last_value = self.state
        self.get_state()
        # check if button clicked since last scan
        # clicked state only valid for 1 scan
        if last_value == 0 and self.state == 1:
            self.clicked = True
        else:
            self.clicked = False

    def was_clicked(self):
        return self.clicked

    def clear_clicked(self):
        self.clicked = False