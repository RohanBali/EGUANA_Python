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
import os, os.path

class TwoDConfig(EguanaConfig):
    
    def __init__(self):
        EguanaConfig.__init__(self)   
        self.buttonName = "Select Directory for 2D EMA"
        self.posPath = ""

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
    		trialName = trial.strip('.pos')
    		if trialNum == int(trialName):
    			trialFound = 1
    			break

    	return trialFound

    def setDirPath(self,path):
        super(TwoDConfig,self).setDirPath(path)
        self.posPath = self.dirPath + '/pos'



    
    
    