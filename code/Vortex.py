# animation for bouncing boxes
from AnimationInterface import AnimationInterface

import utime
import random

from DataHandler import DataHandler


class Vortex(AnimationInterface):

    def __init__(self):
        self.endTime = None
        self.startTime = None
        self.bandColours = None
        self.peakValue = None
        self.oldPower = None
        self.currentPowers = None
        self.numBands = None

    def initialise(self):
        self.numBands = 8
        self.currentPowers = [0 for i in range(self.numBands)]
        self.oldPower = [0 for i in range(self.numBands)]
        self.peakValue = 5000

        self.bandColours = []
        for band in range(self.numBands):
            while True:
                colour = (random.randint(0, 4), random.randint(0, 4), random.randint(0, 4))
                if colour != 0:
                    break
            self.bandColours.append(colour)

        # set a run time for this colour palette
        self.startTime = utime.time()
        self.endTime = self.startTime + 20 + random.randint(0, 60)

    def renderFrame(self):
        # get audio sample
        DataHandler.microphoneHandler.sampleAudio()
        DataHandler.microphoneHandler.getSpectrum()
        # calculate peak and convert fft to 8 bands
        peakReading = 0
        readingsPerBand = 4
        for index in range(self.numBands):
            # check peak and max power in band
            maxPower = 0
            for readingIndex in range(readingsPerBand):
                if DataHandler.microphoneHandler.fft[(readingsPerBand * index) + readingIndex] > peakReading:
                    peakReading = DataHandler.microphoneHandler.fft[(readingsPerBand * index) + readingIndex]
                if maxPower < DataHandler.microphoneHandler.fft[(readingsPerBand * index) + readingIndex]:
                    maxPower = DataHandler.microphoneHandler.fft[(readingsPerBand * index) + readingIndex]

            # scale and cut off bottom powers
            self.currentPowers[index] = ((maxPower / self.peakValue) * 34.0) - 2
            if self.currentPowers[index] < 0:
                self.currentPowers[index] = 0.0
            if self.currentPowers[index] > 32:
                self.currentPowers[index] = 32.0

        # auto gain feature
        if self.peakValue < peakReading:
            self.peakValue = peakReading
        else:
            self.peakValue = (self.peakValue * 0.99) + (peakReading * 0.01)
        if self.peakValue < 6000:
            self.peakValue = 6000

        for band in range(self.numBands):
            boxSize = (band + 1) * 2
            boxColour = self.bandColours[band]
            boxIntensity = self.currentPowers[band] if self.currentPowers[band] > self.oldPower[band] else \
            self.oldPower[band]
            self.oldPower[band] = boxIntensity - 0.5
            if self.oldPower[band] < 0:
                self.oldPower[band] = 0
            boxIntensity += 0  # minimum intensity
            boxColour = tuple(int(i * boxIntensity) for i in boxColour)
            boxColour = DataHandler.lightboxHandler.rgb888ToRgb565(boxColour)
            DataHandler.lightboxHandler.pixelFrameBuffer.rect(7 - band, 7 - band, boxSize, boxSize, boxColour)

        # check if time to change colour pallete
        if utime.time() > self.endTime:
            self.initialise()

    def shutdown(self):
        pass

    def getName(self):
        return "Bouncing Boxes"
