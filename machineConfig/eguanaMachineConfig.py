# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 11:00:13 2016

@author: rohanbali
"""
from tkinter import  DISABLED, NORMAL

class EguanaMachineConfig():

    def __init__(self):
        self.buttonName = ""
        self.setupPlotAndFilterStates()
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


    def getDataForTrialNumber(self,trailNum):
        return




