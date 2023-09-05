from LightboxHandler import LightboxHandler
from DataHandler import DataHandler
import utime
import random


class Box(object):
    """Bouncing box."""

    def __init__(self, screen_width, screen_height, size, display, color):

        self.size = size
        self.w = screen_width
        self.h = screen_height
        self.display = display
        self.color = color
        # Generate non-zero random speeds
        random.seed(utime.ticks_cpu())
        self.x_speed = random.random()*2 - 1
        self.y_speed = random.random()*2 - 1

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


boxes = [Box(16,
             16,
             random.randint(3, 6),
             DataHandler.lightboxHandler.pixelFrameBuffer,
             DataHandler.lightboxHandler.rgb888ToRgb565((random.randint(0, 1) * 128, random.randint(0, 1) * 128,
                                                         random.randint(0, 1) * 128))) for i in range(5)]

while True:
    boxes = [Box(16,
                 16,
                 random.randint(3, 6),
                 DataHandler.lightboxHandler.pixelFrameBuffer,
                 DataHandler.lightboxHandler.rgb888ToRgb565((random.randint(0, 1) * 128, random.randint(0, 1) * 128,
                                                         random.randint(0, 1) * 128))) for i in range(5)]
    while random.randint(0,200) != 0:
        for b in boxes:
            b.update_pos()
            b.draw()

        DataHandler.lightboxHandler.render()
        DataHandler.lightboxHandler.pixelFrameBuffer.fill(DataHandler.lightboxHandler.rgb888ToRgb565((16,16,16)))
