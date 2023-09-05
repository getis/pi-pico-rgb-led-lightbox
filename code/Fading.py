# animation for fading lightbox
from AnimationInterface import AnimationInterface

import utime
import random

from DataHandler import DataHandler

class Fading(AnimationInterface):

    def __init__(self):
        self.maxFadeSpeed = None
        self.fadeSpeedStep = None
        self.fadeSpeed = None
        self.maxBrightness = None
        self.endTime = None
        self.startTime = None
        self.baseColour = None
        self.brightness = None

    def initialise(self):
        self.baseColour = 0b111111
        self.maxBrightness = 48
        self.brightnessStep = 2
        self.brightness = 0
        self.fadeSpeed = 0
        self.fadeSpeedStep = 100
        self.maxFadeSpeed = 1000

        self.changeColour()
        self.lastFadeTime = utime.ticks_ms()

        self.state = 1  # increasing, -1 = decreasing

    def renderFrame(self):

        if utime.ticks_diff(utime.ticks_ms(), self.lastFadeTime) > self.fadeSpeed:
            # process next fade
            if self.state == 1:  # increasing brightness
                self.brightness += self.brightnessStep
                if self.brightness > self.maxBrightness:
                    self.brightness = self.maxBrightness
                    self.state = -1  # decreasing
            else:  # decreasing
                self.brightness -= self.brightnessStep
                if self.brightness < 0:
                    self.brightness = 0
                    self.changeColour()
                    self.state = 1  # increasing

            self.renderColour()
            self.lastFadeTime = utime.ticks_ms()

        # check buttons
        if DataHandler.buttonHandler.buttons['btn_up'].was_clicked():
            self.fadeSpeed += self.fadeSpeedStep
        elif DataHandler.buttonHandler.buttons['btn_down'].was_clicked():
            self.fadeSpeed -= self.fadeSpeedStep
        if self.fadeSpeed < 0:
            self.fadeSpeed = 0
        elif self.fadeSpeed > self.maxFadeSpeed:
            self.fadeSpeed = self.maxFadeSpeed

        print(self.fadeSpeed)

    def changeColour(self):
        # set colour
        self.baseColour = random.randint(1, 63)  # not black

    def renderColour(self):
        # get colour components from base
        red = (self.baseColour >> 4) & 0b11  # bits 4,5
        green = (self.baseColour >> 2) & 0b11  # bits 2,3
        blue = self.baseColour & 0b11  # bits 0,1

        # multiply by brightness
        red = red * self.brightness
        green = green * self.brightness
        blue = blue * self.brightness

        currentColour = DataHandler.lightboxHandler.rgb888ToRgb565((red, green, blue))

        # fill screen
        DataHandler.lightboxHandler.pixelFrameBuffer.fill(currentColour)

    def shutdown(self):
        pass

    def getName(self):
        return "Lamp"