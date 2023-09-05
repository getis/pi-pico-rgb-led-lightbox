# animation for multicolour lightbox
from AnimationInterface import AnimationInterface

import utime
import random

from DataHandler import DataHandler

class Lamp(AnimationInterface):

    def __init__(self):
        self.endTime = None
        self.startTime = None
        self.baseColour = None
        self.brightness = None

    def initialise(self):
        self.baseColour = 0b111111
        self.maxBrightness = 48
        self.brightness = 16

    def renderFrame(self):

        # get colour components from base
        red = (self.baseColour >> 4) & 0b11  # bits 4,5
        green = (self.baseColour >> 2) & 0b11 #bits 2,3
        blue = self.baseColour & 0b11  # bits 0,1

        # multiply by brightness
        red = red * self.brightness
        green = green * self.brightness
        blue = blue * self.brightness

        currentColour = DataHandler.lightboxHandler.rgb888ToRgb565((red, green, blue))

        # fill screen
        DataHandler.lightboxHandler.pixelFrameBuffer.fill(currentColour)

        # check buttons
        if DataHandler.buttonHandler.buttons['btn_left'].was_clicked():
            self.baseColour -= 1
        elif DataHandler.buttonHandler.buttons['btn_right'].was_clicked():
            self.baseColour += 1
        self.baseColour = self.baseColour % 64

        if DataHandler.buttonHandler.buttons['btn_up'].was_clicked():
            self.brightness += 4
        elif DataHandler.buttonHandler.buttons['btn_down'].was_clicked():
            self.brightness -= 4
        if self.brightness < 0:
            self.brightness = 0
        elif self.brightness > self.maxBrightness:
            self.brightness = self.maxBrightness



    def shutdown(self):
        pass

    def getName(self):
        return "Lamp"