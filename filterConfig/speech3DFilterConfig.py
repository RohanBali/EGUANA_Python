from filterConfig.eguanaFilterConfig import EguanaFilterConfig

class Speech3DFilterConfig(EguanaFilterConfig):
    
    def __init__(self):
        EguanaFilterConfig.__init__(self)   
        self.name = "Speech 3D Filter"
