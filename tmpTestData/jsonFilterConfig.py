from filterConfig.eguanaFilterConfig import EguanaFilterConfig

class JsonFilterConfig(EguanaFilterConfig):
    
    def __init__(self):
        EguanaFilterConfig.__init__(self)   
        self.name = "JSON Filter"
