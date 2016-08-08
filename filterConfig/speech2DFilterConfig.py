from filterConfig.eguanaFilterConfig import EguanaFilterConfig

class Speech2DFilterConfig(EguanaFilterConfig):
    
    def __init__(self):
        EguanaFilterConfig.__init__(self)   
        self.name = "Speech 2D Filter"