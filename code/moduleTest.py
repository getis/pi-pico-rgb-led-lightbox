# tests the module version of animations
import utime

from BouncingBoxes import BouncingBoxes
from Fading import Fading
from Lamp import Lamp
from Life import Life
from Spectrum import Spectrum
from Vortex import Vortex

from DataHandler import DataHandler
import _thread

# register modules
DataHandler.registerModule(Lamp())
DataHandler.registerModule(Fading())
DataHandler.registerModule(BouncingBoxes())
DataHandler.registerModule(Life())
DataHandler.registerModule(Spectrum())
DataHandler.registerModule(Vortex())

# initialise module
DataHandler.modules[DataHandler.runningModule].initialise()


def runAminationModule():
    runState = 1  # running
    while True:
        # update buttons
        DataHandler.buttonHandler.scanButtons()

        if runState == 1:
            DataHandler.modules[DataHandler.runningModule].renderFrame()
            # wait for last frame to render
            while DataHandler.lightboxHandler.runningFrameRender:
                pass
            # request new frame to be rendered
            DataHandler.lightboxHandler.setFrameRenderRequest()
            # wait for data copy
            while not DataHandler.lightboxHandler.okToRenderNextFrame():
                pass

            # ok button cycles running animation
            if DataHandler.buttonHandler.buttons['btn_ok'].was_clicked():
                DataHandler.runningModule = (DataHandler.runningModule + 1) % len(DataHandler.modules)
                # initialise module
                DataHandler.modules[DataHandler.runningModule].initialise()

        elif runState == 0:  # off
            pass

        # check menu button for on / off
        if DataHandler.buttonHandler.buttons['btn_menu'].was_clicked():
            if runState == 1:  # currently running
                runState = 0  # off
                DataHandler.lightboxHandler.pixelFrameBuffer.fill(0)  # turn off screen
                DataHandler.lightboxHandler.render()
            elif runState == 0:  # currently off
                runState = 1  # running
                # initialise curent module
                DataHandler.modules[DataHandler.runningModule].initialise()

def handleFrameRendering(id):
    while True:
        # wait for next frame render request
        while not DataHandler.lightboxHandler.runningFrameRender:
            pass
        DataHandler.lightboxHandler.render()


# start render task on core 1
_thread.start_new_thread(handleFrameRendering, (2,))

# run main loop on core 0
runAminationModule()
