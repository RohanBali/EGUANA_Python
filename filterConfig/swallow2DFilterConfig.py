from filterConfig.eguanaFilterConfig import EguanaFilterConfig

class Swallow2DFilterConfig(EguanaFilterConfig):
    
    def __init__(self):
        EguanaFilterConfig.__init__(self)   
        self.name = "Swallow 2D Filter"
