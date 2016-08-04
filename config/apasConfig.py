# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 11:01:25 2016

@author: rohanbali
"""

from config.eguanaConfig import EguanaConfig

class ApasConfig(EguanaConfig):
    
    def __init__(self):
        EguanaConfig.__init__(self)   
        self.buttonName = "Select Directory for the APAS system"
        print("ok")
    
    def readHeadFile(self,filename):
        return 1
        
    def whatsMyName(self):
        print("ThreeDConfig")
