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
import numpy

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



    def getDataForTrialNumber(self,trialNum):

        filePath = self.posPath + "/" + "%04d"%trialNum + '.pos'
        fileObj = open(filePath,'r',encoding='iso-8859-1')
        firstLine = fileObj.readline()
        secondLine = fileObj.readline()
        offsetVal = int(secondLine)
        fileObj.seek(offsetVal,0)
        dataArray = numpy.fromfile(fileObj,numpy.float32)
        numRows = int(len(dataArray)/112)
        dataMatrix = numpy.zeros((numRows,112))

        print(" Num Rows - " + str(numRows))

        for i in range(len(dataArray)):
            dataMatrix[int(i/112)][i%112] = dataArray[i]






        












    
    