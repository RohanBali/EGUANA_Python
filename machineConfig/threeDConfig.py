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
import glob
import re

class ThreeDConfig(EguanaMachineConfig):

    name = "3D EMA"
    number_of_coils = 16
    channel_names = ['X','Y','Z','Phi','Theta','RMS','Extra']
    relevant_channels = [True,True,True,True,True,False,False]

    def __init__(self,dirPath):
        EguanaMachineConfig.__init__(self,dirPath)
        self.buttonName = "Select Directory for 3D EMA"
        self.getAllowedFilters = ['speech3DFilterConfig.py','swallow3DFilterConfig.py']
        
    def whatsMyName(self):
        print("ThreeDConfig")

    def setupPlotAndFilterStates(self):
        self.plot3DKButtonState = 'normal'
        self.plot3DDstButtonState = 'normal'
        self.plot3DDpButtonState = 'normal'
        self.plot2DKButtonState = 'disabled'
        self.plot2DDstButtonState = 'disabled'
        self.plot2DDpButtonState = 'disabled'

    
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
 

    def getDataForTrialNumber(self,trialNum):

        filePath = self.posPath + "/" + "%04d"%trialNum + '.pos'
        fileObj = open(filePath,'r',encoding='iso-8859-1')
        firstLine = fileObj.readline()
        secondLine = fileObj.readline()
        offsetVal = int(secondLine)
        fileObj.seek(offsetVal,0)
        dataArray = numpy.fromfile(fileObj,numpy.float32)
        numRows = int(len(dataArray)/112)
        dataMatrix = dataArray.reshape((numRows,16,7))
        dataMatrix = numpy.swapaxes(dataMatrix,0,2)
        dataMatrix = numpy.swapaxes(dataMatrix,0,1)

        return dataMatrix


    def _defineSamplingRate(self):


        for i in range(self.getNumTrials()):
            if self.ifTrialExists(i):
                filePath = self.posPath + "/" + "%04d"%i + '.pos'
                fileObj = open(filePath,'r',encoding='iso-8859-1')
                firstLine = fileObj.readline()
                secondLine = fileObj.readline()
                thirdLine = fileObj.readline()
                fourthLine = fileObj.readline()
                samplingRateString = re.sub('[^0-9]','', fourthLine)

                self.kinematic_samplingrate = int(samplingRateString)

                break


    def getNumTrials(self):
        os.chdir(self.posPath)
        return len(glob.glob("*.pos"))






        