# class to hold global app data
from ButtonHandler import ButtonHandler
from LightboxHandler import LightboxHandler
from MicrophoneHandler import MicrophoneHandler


class DataHandler:
    # Lightbox handler instance
    lightboxHandler = LightboxHandler(16, 16, 0)

    # Microphone handler instance
    microphoneHandler = MicrophoneHandler(26)

    # holds references to the available modules
    modules = []
    # select running module
    runningModule = 0

    # Button Handler instance
    buttonHandler = ButtonHandler()

    @classmethod
    # register a module as available
    def registerModule(cls, module):
        cls.modules.append(module)

