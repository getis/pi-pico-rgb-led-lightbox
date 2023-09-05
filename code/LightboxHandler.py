# class to handle the lightbox neopixel interface

import framebuf
import neopixel
from machine import Pin


class LightboxHandler:

    # constructor
    def __init__(self, width, height, pin):
        self.width = width
        self.height = height
        self.numPixels = self.width * self.height
        self.pin = pin

        # signals to show state of rendering process
        self.runningFrameRender = False
        self.runningFrameCopy = False

        # setup neopixel pin
        self.neopixels = neopixel.NeoPixel(Pin(self.pin), self.numPixels)

        # setup pixel byte arrays
        # these store raw RGB values for each neopixel
        # live rendering array
        self.pixelBytes = bytearray(self.numPixels * 2)  # RGB565 uses 2 bytes per pixel
        # render buffer
        self.renderBuffer = bytearray(self.numPixels * 2)  # RGB565 uses 2 bytes per pixel

        # setup frame buffers
        self.pixelFrameBuffer = framebuf.FrameBuffer(self.pixelBytes, self.width, self.height, framebuf.RGB565)
        self.renderFrameBuffer = framebuf.FrameBuffer(self.renderBuffer, self.width, self.height, framebuf.RGB565)


    def setFrameRenderRequest(self):
        self.runningFrameRender = True
        self.runningFrameCopy = True

    def okToRenderNextFrame(self):
        return not self.runningFrameCopy

    # draws framebuffers to neopixels
    # first pixel in bottom left
    # order alternates direction up the pixels array
    # x, y coords use top left as (0, 0)
    def render(self):
        # signal frame rendering in process
        self.runningFrameRender = True
        # copy live frame to render frame
        self.runningFrameCopy = True
        # self.renderFrameBuffer.blit(self.pixelFrameBuffer, 0, 0)
        self.renderBuffer[:] = self.pixelBytes
        self.runningFrameCopy = False
        row = self.height - 1
        column = 0
        neopixelIndex = 0
        colDirection = 1
        while row >= 0:
            if colDirection == 1:
                # moving to right
                while column < self.width:
                    col565 = self.renderFrameBuffer.pixel(column, row)
                    red, green, blue = self.rgb565toRgb888(col565)
                    self.neopixels[neopixelIndex] = (red, green, blue)
                    neopixelIndex += 1
                    column += colDirection
                colDirection = -1
                column = self.width - 1
            elif colDirection == -1:
                # moving to left
                while column >= 0:
                    col565 = self.renderFrameBuffer.pixel(column, row)
                    red, green, blue = self.rgb565toRgb888(col565)
                    self.neopixels[neopixelIndex] = (red, green, blue)
                    neopixelIndex += 1
                    column += colDirection

                colDirection = 1
                column = 0

            row -= 1

        self.neopixels.write()
        self.runningFrameRender = False

    # rgb translations

    def rgb888ToRgb565(self, rgbColour888):
        # get 565 components
        red = (rgbColour888[0] >> 3) & 0x1f
        green = (rgbColour888[1] >> 2) & 0x3f
        blue = (rgbColour888[2] >> 3) & 0x1f
        # construct 565 16 bit integer
        return (red << 11) + (green << 5) + (blue)

    def rgb565toRgb888(self, rgbColour565: int):
        # get components
        red = (rgbColour565 & 0xf800) >> 8
        green = (rgbColour565 & 0x7e0) >> 3
        blue = (rgbColour565 & 0x1f) << 3
        return (red, green, blue)
