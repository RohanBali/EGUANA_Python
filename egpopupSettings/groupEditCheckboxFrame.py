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

        for i in range(len(headFilterFilenameList)):
            tmpFrame = Frame(self);
            tmpFrame.grid(row=1+i,column=0,sticky=N+S+E+W)
            tmpFrame.rowconfigure(0,weight=1)
            tmpFrame.columnconfigure(0,weight=1)
            tmpFrame.columnconfigure(1,weight=1)
            Checkbutton(tmpFrame).grid(row=0, column=0, sticky=E)
            Label(tmpFrame,text=objectHelper.getHeadFilterNameFromHeadFilterFilename(headFilterFilenameList[i])).grid(row=0,column=1,sticky=W)
            self.rowconfigure(1+i,weight=1)

        for i in range(len(jawFilterFilenameList)):
            tmpFrame = Frame(self);
            tmpFrame.grid(row=1+i,column=1,sticky=N+S+E+W)
            tmpFrame.rowconfigure(0,weight=1)
            tmpFrame.columnconfigure(0,weight=1)
            tmpFrame.columnconfigure(1,weight=1)
            Checkbutton(tmpFrame).grid(row=0, column=0, sticky=E)
            Label(tmpFrame,text=objectHelper.getJawFilterNameFromJawFilterFilename(jawFilterFilenameList[i])).grid(row=0,column=1,sticky=W)
            self.rowconfigure(1+i,weight=1)

        for i in range(len(moduleFilenameList)):
            tmpFrame = Frame(self);
            tmpFrame.grid(row=1+i,column=2,sticky=N+S+E+W)
            tmpFrame.rowconfigure(0,weight=1)
            tmpFrame.columnconfigure(0,weight=1)
            tmpFrame.columnconfigure(1,weight=1)
            Checkbutton(tmpFrame).grid(row=0, column=0, sticky=E)
            Label(tmpFrame,text=objectHelper.getModuleNameFromModuleFilename(moduleFilenameList[i])).grid(row=0,column=1,sticky=W)
            self.rowconfigure(1+i,weight=1)

