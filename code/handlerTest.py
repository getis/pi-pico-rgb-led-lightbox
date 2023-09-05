from LightboxHandler import LightboxHandler
from DataHandler import DataHandler
import utime

x = 0
y = 0

while True:
    x = (x + 1) % 16
    y = 0
    DataHandler.lightboxHandler.pixelFrameBuffer.fill(DataHandler.lightboxHandler.rgb888ToRgb565((0, 0, 0)))
    DataHandler.lightboxHandler.pixelFrameBuffer.pixel(x, y, DataHandler.lightboxHandler.rgb888ToRgb565((128, 0, 0)))
    DataHandler.lightboxHandler.render()
    utime.sleep(1)
