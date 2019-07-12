# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 11:01:25 2016

@author: rohanbali
"""

from machineConfig.eguanaMachineConfig import EguanaMachineConfig

class ApasConfig(EguanaMachineConfig):
    name = "APAS"

    def __init__(self):
        super(ApasConfig, self).__init__()
        self.machineName = "APAS system"

    def readHeadFile(self,filename):
        return 1

    def whatsMyName(self):
        print("ThreeDConfig")
