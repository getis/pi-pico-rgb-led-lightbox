# animation for bouncing boxes
from AnimationInterface import AnimationInterface

import utime
import random

from DataHandler import DataHandler


class Box(object):

    def __init__(self, screen_width, screen_height, size, display, color):

        self.size = size
        self.w = screen_width
        self.h = screen_height
        self.display = display
        self.color = color
        # Generate non-zero random speeds
        random.seed(utime.ticks_cpu())
        self.x_speed = random.random() * 2 - 1
        self.y_speed = random.random() * 2 - 1

        self.x = self.w / 2.0
        self.y = self.h / 2.0

    def update_pos(self):
        self.x += self.x_speed
        self.y += self.y_speed

        # check limits
        if self.x < 0:
            self.x = 0
            self.x_speed = -self.x_speed
        elif (self.x + self.size - 1) >= self.w:
            self.x = self.w - self.size
            self.x_speed = -self.x_speed

        if self.y < 0:
            self.y = 0
            self.y_speed = -self.y_speed
        elif (self.y + self.size - 1) >= self.h:
            self.y = self.h - self.size
            self.y_speed = -self.y_speed

    def draw(self):
        x = int(self.x)
        y = int(self.y)
        size = self.size
        self.display.rect(x, y, size, size, self.color)


class BouncingBoxes(AnimationInterface):

    def __init__(self):
        self.endTime = None
        self.startTime = None
        self.boxes = None

    def initialise(self):
        self.boxes = []
        for box in range(5):
            while True:
                newColour = DataHandler.lightboxHandler.rgb888ToRgb565(
                    (random.randint(0, 1) * 16, random.randint(0, 1) * 16,
                     random.randint(0, 1) * 16))
                if newColour != 0:
                    break
            self.boxes.append(Box(16,
                                  16,
                                  random.randint(3, 6),
                                  DataHandler.lightboxHandler.pixelFrameBuffer, newColour))

        # set a run time for this colour palette
        self.startTime = utime.time()
        self.endTime = self.startTime + 20 + random.randint(0, 60)

    def renderFrame(self):
        # clear screen
        DataHandler.lightboxHandler.pixelFrameBuffer.fill(DataHandler.lightboxHandler.rgb888ToRgb565((0, 0, 0)))

        # handle boxes
        for b in self.boxes:
            b.update_pos()
            b.draw()

        # check if time to change colour pallete
        if utime.time() > self.endTime:
            self.initialise()

    def shutdown(self):
        pass

    def getName(self):
        return "Bouncing Boxes"
