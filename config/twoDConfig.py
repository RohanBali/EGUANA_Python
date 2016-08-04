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

    def isDirectoryValid(self, path):
    	fileFound = 0
    	if 'pos' in os.listdir(path):
    		posPath = path + '/pos'	
    		for fileName in os.listdir(posPath):
    			if fileName.endswith('.pos'):
    				fileFound = 1
    				break
    	return fileFound




    
    
    