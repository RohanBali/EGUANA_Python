# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 09:36:50 2016

@author: rohanbali
"""

#3d EMA class . /config

#name
#how to read functions

from config.eguanaConfig import EguanaConfig

class ThreeDConfig(EguanaConfig):
    
    def __init__(self):
        self.buttonName = "Select Directory for 3D EMA"
        print("ok")
    
    def readHeadFile(self,filename):
        return 1
        
    def whatsMyName(self):
        print("ThreeDConfig")
