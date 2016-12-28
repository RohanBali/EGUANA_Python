# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 11:00:13 2016

@author: rohanbali
"""
from tkinter import  DISABLED, NORMAL
import sys

class EguanaMachineConfig():
    name = ""
    number_of_coils = 0
    channel_names = []
    relevant_channels = []


    def __init__(self):
        #self.setupPlotAndFilterStates()
        self.dirPath = ""
        
    def isDirectoryValid(self, path):
        return

    def ifTrialExists(self, trialNum):
        return

    def getDataForTrialNumber(self,trailNum):
        return

    def setDirPath(self,path):
        self.dirPath = path

    def getFilename(self):
        fullPath =  sys.modules[self.__class__.__module__].__file__
        components = fullPath.split('/')
        return components[-1]
