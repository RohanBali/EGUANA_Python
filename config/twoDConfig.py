# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 09:43:29 2016

@author: rohanbali
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 09:36:50 2016

@author: rohanbali
"""
from config.eguanaConfig import EguanaConfig


class TwoDConfig(EguanaConfig):
    
    def __init__(self):
        EguanaConfig.__init__(self)   
        self.buttonName = "Select Directory for 2D EMA"

    
    
    