# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 11:01:25 2016

@author: rohanbali
"""

from machineConfig.eguanaMachineConfig import EguanaMachineConfig

class TestConfig(EguanaMachineConfig):
    name = 'Test'

    def __init__(self):
        super(TestConfig, self).__init__()
        self.machineName = "Test"

    def readHeadFile(self,filename):
        return 1

    def whatsMyName(self):
        print("ThreeDConfig")
