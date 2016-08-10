# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 11:01:25 2016

@author: rohanbali
"""

from machineConfig.eguanaMachineConfig import EguanaMachineConfig

class TestConfig(EguanaMachineConfig):
    
    def __init__(self):
        EguanaMachineConfig.__init__(self)   
        self.buttonName = "Select Directory for the test system"
        self.name = "Test"
    
    def readHeadFile(self,filename):
        return 1
        
    def whatsMyName(self):
        print("ThreeDConfig")
