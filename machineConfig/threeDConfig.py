# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 09:36:50 2016

@author: rohanbali
"""

#3d EMA class . /config

#name
#how to read functions

from machineConfig.eguanaMachineConfig import EguanaMachineConfig
from tkinter import  DISABLED, NORMAL
import os, os.path

class ThreeDConfig(EguanaMachineConfig):
    
    def __init__(self):
        EguanaMachineConfig.__init__(self)
        self.buttonName = "Select Directory for 3D EMA"
        self.getAllowedFilters = ['speech3DFilterConfig.py','swallow3DFilterConfig.py']   
    
    def readHeadFile(self,filename):
        return 1
        
    def whatsMyName(self):
        print("ThreeDConfig")

    def setupPlotAndFilterStates(self):
        self.plot3DKButtonState = 'normal'
        self.plot3DDstButtonState = 'normal'
        self.plot3DDpButtonState = 'normal'
        self.plot2DKButtonState = 'disabled'
        self.plot2DDstButtonState = 'disabled'
        self.plot2DDpButtonState = 'disabled'
        self.speech3DFilterButtonState = NORMAL
        self.swallow3DFilterButtonState = NORMAL
        self.speech2DFilterButtonState = DISABLED
        self.swallow2DFilterButtonState = DISABLED
    
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
        super(ThreeDConfig,self).setDirPath(path)
        self.posPath = self.dirPath + '/pos'
 

        