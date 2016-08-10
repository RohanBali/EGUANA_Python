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
        self.setupAllowedFilterFunctions()
        self.dirPath = ""
        self.name = ""


    def setupPlotAndFilterStates(self):
        self.plot3DKButtonState = 'normal'
        self.plot3DDstButtonState = 'normal'
        self.plot3DDpButtonState = 'normal'
        self.plot2DKButtonState = 'normal'
        self.plot2DDstButtonState = 'normal'
        self.plot2DDpButtonState = 'normal'
                
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

    def setupAllowedFilterFunctions(self):

        self.allowedFilterFunctions = []

        with open('config.json') as data_file:    
            data = json.load(data_file)


        className = self.__class__.__name__
        print(className)
        fileName = className[0].lower() + className[1:] + '.py'


        for i in data:
            if i['machineName'] == fileName:
                filterData = i['filterFunctions']
                for j in filterData:
                    filterFunctionName = j['filterApplicationName']
                    self.allowedFilterFunctions.append(self.getFilterObjectFromFunctionName(filterFunctionName))


    def getFilterObjectFromFunctionName(self,filterFunctionName):
        components = filterFunctionName.split('.')
        fileName = components[0]
        className = fileName[0].upper() + fileName[1:]
        module = __import__("filterConfig."+fileName,fromlist=["filterConfig."])                        
        classVar = getattr(module,className)
        classObject = classVar()
        classObject.setupMachineType(self)
        return classObject
