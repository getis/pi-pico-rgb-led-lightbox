# animation for John Conways Game Of Life
import framebuf

from AnimationInterface import AnimationInterface

import utime
import random

from DataHandler import DataHandler


class Life(AnimationInterface):

    def __init__(self):
        self.colourAlive = DataHandler.lightboxHandler.rgb888ToRgb565((0, 128, 0))
        self.colourDead = DataHandler.lightboxHandler.rgb888ToRgb565((0, 0, 0))

    def initialise(self):
        # reset colour
        while True:
            testCol = (random.randint(0, 2) * 32, random.randint(0, 2) * 32, random.randint(0, 2) * 32)
            self.colourAlive = DataHandler.lightboxHandler.rgb888ToRgb565(testCol)
            if self.colourAlive != self.colourDead:
                break
        # clear grid
        DataHandler.lightboxHandler.pixelFrameBuffer.fill(self.colourDead)
        # add live cells
        for cell in range(random.randint(60, 100)):
            DataHandler.lightboxHandler.pixelFrameBuffer.pixel(
                random.randint(0, DataHandler.lightboxHandler.width - 1),
                random.randint(0, DataHandler.lightboxHandler.height - 1),
                self.colourAlive
            )

        # set a max run time for this colour palette
        self.startTime = utime.time()
        self.endTime = self.startTime + 20 + random.randint(0, 60)

    def renderFrame(self):
        numLivingCells = 0
        numChanged = 0
        grid = [[0 for i in range(DataHandler.lightboxHandler.width)] for j in
                range(DataHandler.lightboxHandler.height)]
        for row in range(0, DataHandler.lightboxHandler.height):
            for col in range(0, DataHandler.lightboxHandler.width):
                currentCol = DataHandler.lightboxHandler.pixelFrameBuffer.pixel(col, row)
                currentNeighbours = self.getNeighbours(col, row)
                # rules
                if (currentCol == self.colourAlive) and currentNeighbours < 2:
                    numChanged += 1
                    grid[col][row] = self.colourDead
                elif (currentCol == self.colourAlive) and ((currentNeighbours == 2) or (currentNeighbours == 3)):
                    grid[col][row] = self.colourAlive
                elif (currentCol == self.colourAlive) and (currentNeighbours > 3):
                    numChanged += 1
                    grid[col][row] = self.colourDead
                elif (currentCol == self.colourDead) and (currentNeighbours == 3):
                    numChanged += 1
                    grid[col][row] = self.colourAlive
                elif (currentCol == self.colourDead):
                    grid[col][row] = self.colourDead

                if grid[col][row] != self.colourDead:
                    numLivingCells += 1

        # build new frame
        for row in range(0, DataHandler.lightboxHandler.height):
            for col in range(0, DataHandler.lightboxHandler.width):
                DataHandler.lightboxHandler.pixelFrameBuffer.pixel(col, row, grid[col][row])

        # check for reset
        if (utime.time() > self.endTime) or (numLivingCells == 0) or (numChanged <= 2):
            self.initialise()

    def getNeighbours(self, col, row):
        neighbours = 0
        for testRow in range(row - 1, row + 2):
            for testCol in range(col - 1, col + 2):
                if self.getPixelColour(testCol, testRow) != self.colourDead:
                    neighbours += 1
        return neighbours

    def getPixelColour(self, col, row):
        if (col < 0) or (col >= DataHandler.lightboxHandler.width) or (row < 0) or (
                row >= DataHandler.lightboxHandler.height):
            return self.colourDead
        else:
            return DataHandler.lightboxHandler.pixelFrameBuffer.pixel(col, row)

    def shutdown(self):
        pass

    def getName(self):
        return "Game Of Life"
