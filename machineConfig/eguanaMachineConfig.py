# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 11:00:13 2016

@author: rohanbali
"""
from tkinter import  DISABLED, NORMAL
import os, os.path
import json
import sys

class EguanaMachineConfig():

    def __init__(self):
        self.buttonName = ""
        self.setupPlotAndFilterStates()
        self.dirPath = ""
        self.allowedFilterList =  []


    def setupPlotAndFilterStates(self):
        self.plot3DKButtonState = 'normal'
        self.plot3DDstButtonState = 'normal'
        self.plot3DDpButtonState = 'normal'
        self.plot2DKButtonState = 'normal'
        self.plot2DDstButtonState = 'normal'
        self.plot2DDpButtonState = 'normal'
        self.speech3DFilterButtonState = NORMAL
        self.swallow3DFilterButtonState = NORMAL
        self.speech2DFilterButtonState = NORMAL
        self.swallow2DFilterButtonState = NORMAL
                
    def whatsMyName(self):
        print("EguanaMachineConfig")
        
    def readHeadFile(self,filename):
        return 1

    def isDirectoryValid(self, path):
        return

    def ifTrialExists(self, trialNum):
        return

    def setDirPath(self,path):
        self.dirPath = path   

    def getAllowedFilterFunctionsName(self):

        with open('config.json') as data_file:    
            data = json.load(data_file)


        className = self.__class__.__name__
        fileName = className[0].lower() + className[1:] + '.py'

        filterFunctionNames = []

        for i in data:
            if i['machineName'] == fileName:
                filterData = i['filterFunctions']
                for j in filterData:
                    filterFunctionNames.append(j['filterApplicationName'])


        return filterFunctionNames

    def getAllowedFilterTypesForFilterApplications(self,filterApplication):
        a = 1
