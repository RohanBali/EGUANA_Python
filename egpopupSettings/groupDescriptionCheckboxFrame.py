from tkinter import *
from tkinter import Toplevel, RAISED, Button, TOP, X, NORMAL, DISABLED, S, N, E, W, SUNKEN, Label, OptionMenu
from tkinter.ttk import Notebook
from eguanaModel import EguanaModel
from helpers import jsonHelper, objectHelper

class GroupDescriptionCheckboxFrame(Frame):
    def __init__(self,notebook,groupName):
        Frame.__init__(self,notebook) 
        self.groupName = groupName
        self.enableCheckButtonInt = IntVar()
        Checkbutton(self, text='Enabled', variable=self.enableCheckButtonInt).grid(row=0, column=0, columnspan=3, sticky=N+W)

        Label(self,text="Head Filters").grid(row=1,column=0,sticky=N+S+E+W)
        Label(self,text="Jaw Filters").grid(row=1,column=1,sticky=N+S+E+W)
        Label(self,text="Modules").grid(row=1,column=2,sticky=N+S+E+W)

        headFilterList = jsonHelper.getHeadFiltersListForGroup(groupName)
        jawFilterList = jsonHelper.getJawFiltersListForGroup(groupName)
        moduleList = jsonHelper.getModuleListForGroup(groupName)

        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)

        for i in range(len(headFilterList)):
            Label(self,text=objectHelper.getHeadFilterNameFromHeadFilterFilename(headFilterList[i])).grid(row=2+i,column=0,sticky=N+S+E+W)
            self.rowconfigure(2+i,weight=1)

        for i in range(len(jawFilterList)):
            Label(self,text=objectHelper.getJawFilterNameFromJawFilterFilename(jawFilterList[i])).grid(row=2+i,column=1,sticky=N+S+E+W)
            self.rowconfigure(2+i,weight=1)

        for i in range(len(moduleList)):
            Label(self,text=objectHelper.getModuleNameFromModuleFilename(moduleList[i])).grid(row=2+i,column=2,sticky=N+S+E+W)
            self.rowconfigure(2+i,weight=1)



    def isEnabled(self):
        return self.enableCheckButtonInt.get()
