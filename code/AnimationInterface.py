# base class for animations
# defines methods required

class AnimationInterface:

    def initialise(self):
        # this will be called during the setup process before frames are generated
        raise NotImplementedError

    def renderFrame(self):
        # generate next frame and place in framebuffer
        raise NotImplementedError

    def shutdown(self):
        # clean up at end of run
        raise NotImplementedError

    def getName(self):
        # return display name of module
        raise NotImplementedError
