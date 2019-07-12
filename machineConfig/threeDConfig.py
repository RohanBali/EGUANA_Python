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
    name = "3D EMA"

    def __init__(self):
        super(ThreeDConfig, self).__init__()
        self.machineName = "3D EMA"
        self.getAllowedFilters = ['speech3DFilterConfig.py','swallow3DFilterConfig.py']


    def isDirectoryValid(self, path):
        fileFound = 0
        if 'rawpos' in os.listdir(path):
            posPath = os.path.join(path,'rawpos')
            for fileName in os.listdir(posPath):
                if fileName.endswith('.pos'):
                    fileFound = 1
                    break
        print(fileFound)
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
        dataMatrix = numpy.zeros((numRows,112))

        print(" Num Rows - " + str(numRows))

        for i in range(len(dataArray)):
            dataMatrix[int(i/112)][i%112] = dataArray[i]
