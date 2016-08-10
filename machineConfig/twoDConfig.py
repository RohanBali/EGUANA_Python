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
from machineConfig.eguanaMachineConfig import EguanaMachineConfig
import os, os.path
from tkinter import  DISABLED, NORMAL

class TwoDConfig(EguanaMachineConfig):
    
    def __init__(self):
        EguanaMachineConfig.__init__(self)   
        self.buttonName = "Select Directory for 2D EMA"
        self.posPath = ""
        self.name = "2D EMA"

    def setupPlotAndFilterStates(self):
        self.plot3DKButtonState = 'disabled'
        self.plot3DDstButtonState = 'disabled'
        self.plot3DDpButtonState = 'disabled'
        self.plot2DKButtonState = 'normal'
        self.plot2DDstButtonState = 'normal'
        self.plot2DDpButtonState = 'normal'

    def isDirectoryValid(self, path):
    	fileFound = 0
    	if 'pos' in os.listdir(path):
    		posPath = path + '/pos'	
    		for fileName in os.listdir(posPath):
    			if fileName.endswith('.pos'):
    				fileFound = 1
    				break
    	return fileFound

    def ifTrialExists(self, trialNum):
        trialFound = 0
        for trial in os.listdir(self.posPath):
            if trial.endswith('.pos'):
                trialName = trial.strip('.pos')
                if trialNum == int(trialName):
                    trialFound = 1
                    break

        return trialFound

    def setDirPath(self,path):
        super(TwoDConfig,self).setDirPath(path)
        self.posPath = self.dirPath + '/pos'



    
    
    