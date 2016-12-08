from tkinter import *
from tkinter import Toplevel, RAISED, Button, TOP, X, NORMAL, DISABLED, S, N, E, W, SUNKEN, Label, OptionMenu
from eguanaModel import EguanaModel
from helpers import jsonHelper, objectHelper

class GroupEditCheckboxFrame(Frame):
    def __init__(self,parent,headFilterFilenameList,jawFilterFilenameList,moduleFilenameList):
        Frame.__init__(self,parent) 

        Label(self,text="Head Filters").grid(row=0,column=0,sticky=N+S+E+W)
        Label(self,text="Jaw Filters").grid(row=0,column=1,sticky=N+S+E+W)
        Label(self,text="Modules").grid(row=0,column=2,sticky=N+S+E+W)

        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)

        self.rowconfigure(0,weight=1)

        self.headFilterFilenameList = headFilterFilenameList;
        self.jawFilterFilenameList = jawFilterFilenameList;
        self.moduleFilenameList = moduleFilenameList;

        self.headIntVarList = [];
        self.jawIntVarList = [];
        self.moduleIntVarList = [];

        for i in range(len(headFilterFilenameList)):
            tmpFrame = Frame(self);
            tmpFrame.grid(row=1+i,column=0,sticky=N+S+E+W)
            tmpFrame.rowconfigure(0,weight=1)
            tmpFrame.columnconfigure(0,weight=1)
            tmpFrame.columnconfigure(1,weight=1)
            checkButtonIntVar = IntVar();
            self.headIntVarList.append(checkButtonIntVar)
            Checkbutton(tmpFrame,variable=checkButtonIntVar).grid(row=0, column=0, sticky=E)
            Label(tmpFrame,text=objectHelper.getHeadFilterNameFromHeadFilterFilename(headFilterFilenameList[i])).grid(row=0,column=1,sticky=W)
            self.rowconfigure(1+i,weight=1)

        for i in range(len(jawFilterFilenameList)):
            tmpFrame = Frame(self);
            tmpFrame.grid(row=1+i,column=1,sticky=N+S+E+W)
            tmpFrame.rowconfigure(0,weight=1)
            tmpFrame.columnconfigure(0,weight=1)
            tmpFrame.columnconfigure(1,weight=1)
            checkButtonIntVar = IntVar();
            self.jawIntVarList.append(checkButtonIntVar)
            Checkbutton(tmpFrame,variable=checkButtonIntVar).grid(row=0, column=0, sticky=E)
            Label(tmpFrame,text=objectHelper.getJawFilterNameFromJawFilterFilename(jawFilterFilenameList[i])).grid(row=0,column=1,sticky=W)
            self.rowconfigure(1+i,weight=1)

        for i in range(len(moduleFilenameList)):
            tmpFrame = Frame(self);
            tmpFrame.grid(row=1+i,column=2,sticky=N+S+E+W)
            tmpFrame.rowconfigure(0,weight=1)
            tmpFrame.columnconfigure(0,weight=1)
            tmpFrame.columnconfigure(1,weight=1)
            checkButtonIntVar = IntVar();
            self.moduleIntVarList.append(checkButtonIntVar)
            Checkbutton(tmpFrame,variable=checkButtonIntVar).grid(row=0, column=0, sticky=E)
            Label(tmpFrame,text=objectHelper.getModuleNameFromModuleFilename(moduleFilenameList[i])).grid(row=0,column=1,sticky=W)
            self.rowconfigure(1+i,weight=1)


    def getEnabledHeadFilenames(self):

        headFilenameList = [];

        for i in range(len(self.headFilterFilenameList)):
            checkButton = self.headIntVarList[i];
            if checkButton.get():
                headFilenameList.append(self.headFilterFilenameList[i])

        return headFilenameList

    def getEnabledJawFilenames(self):

        jawFilenameList = [];

        for i in range(len(self.jawFilterFilenameList)):
            checkButton = self.jawIntVarList[i];
            if checkButton.get():
                jawFilenameList.append(self.jawFilterFilenameList[i])

        return jawFilenameList

    def getEnabledModuleFilenames(self):

        moduleFilenameList = [];

        for i in range(len(self.moduleFilenameList)):
            checkButton = self.moduleIntVarList[i];
            if checkButton.get():
                moduleFilenameList.append(self.moduleFilenameList[i])

        return moduleFilenameList


    def setEnabledHeadFilenames(self,enabledHeadFilenameList):

        for fileName in enabledHeadFilenameList:
            if fileName in self.headFilterFilenameList:
                index = self.headFilterFilenameList.index(fileName);
                checkButton = self.headIntVarList[index];
                checkButton.set(1)

    def setEnabledJawFilenames(self,enabledJawFilenameList):

        for fileName in enabledJawFilenameList:
            if fileName in self.jawFilterFilenameList:
                index = self.jawFilterFilenameList.index(fileName);
                checkButton = self.jawIntVarList[index];
                checkButton.set(1)

    def setEnabledModuleFilenames(self,enabledModuleFilenameList):

        for fileName in enabledModuleFilenameList:
            if fileName in self.moduleFilenameList:
                index = self.moduleFilenameList.index(fileName);
                checkButton = self.moduleIntVarList[index];
                checkButton.set(1)










