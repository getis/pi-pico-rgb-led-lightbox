# class to handle the microphone sampling
from machine import ADC, Pin
import utime
from ulab import numpy as np


class MicrophoneHandler:

    def __init__(self, pin):
        # connect the microphone
        self.pin = pin
        self.microphone = ADC(self.pin)
        # will hold the audio samples
        self.samples = []
        self.fft = []

    def sampleAudio(self):
        # clear samples
        self.samples = []
        for sample in range(64):
            # read adc and remove voltage offset
            self.samples.append(self.microphone.read_u16() - 25000)
            utime.sleep_us(200) # sample at 5kHz (very approx!)

    def getSpectrum(self):
        # https://micropython-ulab.readthedocs.io/en/2.1.2/scipy-signal.html
        # https://stackoverflow.com/questions/43284049/spectrogram-of-a-wave-file

        numSamples = len(self.samples)

        # convert sample to numpy array
        npSamples = np.array(self.samples)

        # get real and img parts of fft - magnitude and phase
        fftReal, fftImg = np.fft.fft(np.array(self.samples))

        # get absolute value fft
        fftValues = np.sqrt(fftReal * fftReal + fftImg * fftImg)

        # Scale the fft array by length of sample points so that magnitude does not depend on
        # the length of the signal or on its sampling frequency
        fftValues = fftValues / float(numSamples)

        # only use first half of fft values
        numUniquePoints = numSamples // 2
        fftValues = fftValues[0:numUniquePoints]
        #fftValues[0] = fftValues[1] # dc offset

        self.fft = fftValues