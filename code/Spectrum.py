# animation for bouncing boxes
from AnimationInterface import AnimationInterface

import utime
import random

from DataHandler import DataHandler


class Spectrum(AnimationInterface):

    def __init__(self):
        self.endTime = None
        self.startTime = None
        self.peakValue = None
        self.oldTops = None
        self.currentTops = None
        self.numBands = None

    def initialise(self):
        self.numBands = 16
        self.currentTops = [0 for i in range(self.numBands)]
        self.oldTops = [0 for i in range(self.numBands)]
        self.peakValue = 5000

        # set a run time for this colour palette
        self.startTime = utime.time()
        self.endTime = self.startTime + 20 + random.randint(0, 60)

    def renderFrame(self):
        # get audio sample
        DataHandler.microphoneHandler.sampleAudio()
        DataHandler.microphoneHandler.getSpectrum()
        # calculate peak and convert fft to 16 bands
        peakReading = 0
        readingsPerBand = 2
        for index in range(self.numBands):
            # check peak and max power in band
            maxPower = 0
            for readingIndex in range(readingsPerBand):
                if DataHandler.microphoneHandler.fft[(readingsPerBand * index) + readingIndex] > peakReading:
                    peakReading = DataHandler.microphoneHandler.fft[(readingsPerBand * index) + readingIndex]
                if maxPower < DataHandler.microphoneHandler.fft[(readingsPerBand * index) + readingIndex]:
                    maxPower = DataHandler.microphoneHandler.fft[(readingsPerBand * index) + readingIndex]

            # scale and cut off bottom powers
            self.currentTops[index] = ((maxPower / self.peakValue) * 17.0) - 2
            if self.currentTops[index] > 15:
                self.currentTops[index] = 15

            # auto gain feature
            if self.peakValue < peakReading:
                self.peakValue = peakReading
            else:
                self.peakValue = (self.peakValue * 0.99) + (peakReading * 0.01)
            if self.peakValue < 6000:
                self.peakValue = 6000

        # render bands
        currentColour = DataHandler.lightboxHandler.rgb888ToRgb565((0,128,0))
        oldColour = DataHandler.lightboxHandler.rgb888ToRgb565((64,0,0))

        for column in range(16):
            # check old top value
            if self.oldTops[column] <= self.currentTops[column]:
                self.oldTops[column] = self.currentTops[column]
            # draw current bar
            for pixel in range(int(self.currentTops[column])):
                DataHandler.lightboxHandler.pixelFrameBuffer.pixel(column, 15-pixel, currentColour)
            # draw old bar
            for pixel in range(int(self.currentTops[column] + 1), int(self.oldTops[column])):
                DataHandler.lightboxHandler.pixelFrameBuffer.pixel(column, 15 - pixel, oldColour)
            # blank top bar
            for pixel in range(int(self.oldTops[column] + 1), 16):
                DataHandler.lightboxHandler.pixelFrameBuffer.pixel(column, 15 - pixel, 0)
            # reduce old top
            self.oldTops[column] = self.oldTops[column] - 1


    def shutdown(self):
        pass

    def getName(self):
        return "Bouncing Boxes"