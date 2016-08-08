from filterConfig.eguanaFilterConfig import EguanaFilterConfig

class Swallow3DFilterConfig(EguanaFilterConfig):
    
    def __init__(self):
        EguanaFilterConfig.__init__(self)
        self.name = "Swallow 3D Filter"
