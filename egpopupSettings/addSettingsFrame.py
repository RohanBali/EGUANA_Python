from tkinter import *
from tkinter import Toplevel, RAISED, Button, TOP, X, NORMAL, DISABLED, S, N, E, W, SUNKEN, Label, OptionMenu, BOTH, messagebox
from tkinter.ttk import Notebook

import subprocess
import os.path
import json

from eguanaModel import EguanaModel

from tests.machineConfigTest import MachineConfigTest
from tests.filterTypesConfigTest import FilterTypesConfigTest

from egpopupSettings.filterTypeCheckboxFrame import FilterTypeCheckboxFrame
from egpopupSettings.filterFunctionCheckboxFrame import FilterFunctionCheckboxFrame

from egpopupSettings.groupDescriptionCheckboxFrame import GroupDescriptionCheckboxFrame

from helpers import jsonHelper

class AddSettingsFrame(Frame):

    def __init__(self, notebook, parent):
        Frame.__init__(self,notebook)
        
        self.parent = parent
        
        self.currentTypeValue = None
        self.currentMachineTypeValue = None
        self.currentFilterFunctionValue = None
        self.currentHeadFilterTypeValue = None
        self.currentJawFilterTypeValue = None

        self.setupFrame()

    def setupFrame(self):
        dropList = ['Machine', 'Head Filter','Jaw Filter','Module']
        dropTitle = StringVar()
        dropTitle.set('Select Type')
        drop = OptionMenu(self, dropTitle, *dropList, command=self.selectTypeCallback)
        drop.grid(row=1, column=0, columnspan=4, sticky='ew')
        
        self.currentValue = None

        for row in range(0, 5):
            self.rowconfigure(row, weight=1)

        for col in range(0, 4):
            self.columnconfigure(col, weight=1)

    def selectTypeCallback(self, value):
        if value != self.currentValue:
            self.currentValue = value

            for i in range(2, self.grid_size()[1]):
                for element in self.grid_slaves(i, None):
                    element.grid_forget()

            if value == 'Machine':
                loadButton = Button(self, text='Load config file', relief=RAISED, command=lambda: self.machineLoadButtonPressed(loadButton))
                loadButton.grid(row=2, column=0, columnspan=4, sticky=E+W)

            elif value == 'Head Filter':
                loadButton = Button(self, text='Load config file', relief=RAISED, command=lambda:self.headFilterTypeLoadButtonPressed(loadButton))
                loadButton.grid(row=2, column=0, columnspan=4, sticky=E+W)

            elif value == 'Jaw Filter':
                loadButton = Button(self, text='Load config file', relief=RAISED, command=lambda:self.jawFilterTypeLoadButtonPressed(loadButton))
                loadButton.grid(row=2, column=0, columnspan=4, sticky=E+W)

            else:
                loadButton = Button(self, text='Load config file', relief=RAISED, command=lambda:self.moduleLoadButtonPressed(loadButton))
                loadButton.grid(row=2, column=0, columnspan=4, sticky=E+W)
                return 0

    def machineLoadButtonPressed(self, loadButton):
        filePath = filedialog.askopenfilename(filetypes=[('Python file','*.py')])
        
        if filePath != '':
            components = filePath.split('/')
            fileName = components[-1]

            if os.path.isfile(os.getcwd()+'/machineConfig/'+fileName) == False:
                # [isValid, errorString] = MachineConfigTest(filePath).runTests() //TODO
                isValid = 1

                if isValid:
                    loadButton.config(text=filePath)

                    groupDesctiptionNotebook = Notebook(self)
                    groupDesctiptionNotebook.grid(row=3, column=0, columnspan=4, sticky=E+W)
                    

                    tabNameList = jsonHelper.getAllGroups()
                    groupDescriptionFrameList = [];

                    for tabName in tabNameList:
                        groupDescriptionFrame = GroupDescriptionCheckboxFrame(groupDesctiptionNotebook, tabName)
                        groupDescriptionFrameList.append(groupDescriptionFrame)
                        groupDescriptionFrame.pack(fill=BOTH, expand=True)
                        groupDesctiptionNotebook.add(groupDescriptionFrame, text=tabName)
                      

                    Button(self, text='Apply & Close', relief=RAISED, command=lambda: self.applyMachineButtonPressed(filePath, groupDescriptionFrameList)).grid(row=4,column=1,columnspan=1,sticky=S+E)
                
                else:
                    messagebox.showinfo("Error", errorString)

            else:
                messagebox.showinfo("Error", "File already exists in machineConfig directory: " + fileName)

    def headFilterTypeLoadButtonPressed(self, loadButton):
        filePath = filedialog.askopenfilename()
        if filePath:
            components = filePath.split('/')
            fileName = components[-1]

            if not os.path.isfile(os.getcwd()+'/filterTypesConfig/headFilters/'+fileName):
                # [isValid, errorString] = FilterTypesConfigTest(filePath).runTests()
                isValid = True
                
                if isValid:
                    loadButton.config(text=filePath)
                    self.filterTypeLoadButtonPressed(filePath,'Head')
                
                else:
                    messagebox.showinfo("Error","")
            else:
                messagebox.showinfo("Error", "File already exists in directory: " + fileName)

    def jawFilterTypeLoadButtonPressed(self, loadButton):
        filePath = filedialog.askopenfilename()
        if filePath:
            components = filePath.split('/')
            fileName = components[-1]

            if not os.path.isfile(os.getcwd()+'/filterTypesConfig/jawFilters/'+fileName):
                # [isValid, errorString] = FilterTypesConfigTest(filePath).runTests()
                isValid = True
                
                if isValid:
                    loadButton.config(text=filePath)
                    self.filterTypeLoadButtonPressed(filePath,'Jaw')
                
                else:
                    messagebox.showinfo("Error","")
            else:
                messagebox.showinfo("Error", "File already exists in directory: " + fileName)

    def filterTypeLoadButtonPressed(self, filePath,filterType):
        groupDesctiptionNotebook = Notebook(self)
        groupDesctiptionNotebook.grid(row=3, column=0, columnspan=4, sticky=E+W)

        tabNameList = jsonHelper.getAllGroups()
        groupDescriptionFrameList = [];

        for tabName in tabNameList:
            groupDescriptionFrame = GroupDescriptionCheckboxFrame(groupDesctiptionNotebook, tabName)
            groupDescriptionFrameList.append(groupDescriptionFrame)
            groupDescriptionFrame.pack(fill=BOTH, expand=True)
            groupDesctiptionNotebook.add(groupDescriptionFrame, text=tabName)
          
        Button(self, text='Apply & Close',relief=RAISED,command=lambda:self.applyFilterTypeButtonPressed(filePath, groupDescriptionFrameList, filterType)).grid(row=4,column=1,columnspan=1,sticky=S+E)

    def moduleLoadButtonPressed(self,loadButton):
        filePath = filedialog.askopenfilename(filetypes=[('Python file','*.py')])
        
        if filePath:
            components = filePath.split('/')
            fileName = components[-1]

            if not os.path.isfile(os.getcwd()+'/moduleConfig/'+fileName):
                # [isValid, errorString] = MachineConfigTest(filePath).runTests() //TODO
                isValid = True

                if isValid:
                    loadButton.config(text=filePath)

                    groupDesctiptionNotebook = Notebook(self)
                    groupDesctiptionNotebook.grid(row=3, column=0, columnspan=4, sticky=E+W)
                    
                    tabNameList = jsonHelper.getAllGroups()
                    groupDescriptionFrameList = [];

                    for tabName in tabNameList:
                        groupDescriptionFrame = GroupDescriptionCheckboxFrame(groupDesctiptionNotebook, tabName)
                        groupDescriptionFrameList.append(groupDescriptionFrame)
                        groupDescriptionFrame.pack(fill=BOTH, expand=True)
                        groupDesctiptionNotebook.add(groupDescriptionFrame, text=tabName)
                      
                    Button(self,text='Apply & Close',relief=RAISED, command=lambda: self.applyModuleButtonPressed(filePath, groupDescriptionFrameList)).grid(row=4,column=1,columnspan=1,sticky=S+E)
                
                else:
                    messagebox.showinfo("Error", errorString)

            else:
                messagebox.showinfo("Error", "File already exists in moduleConfig directory: " + fileName)

    def applyMachineButtonPressed(self, filePath, groupDescriptionFrameList):
        components = filePath.split('/')
        fileName = components[-1]

        groupNameList = []

        for groupDescriptionFrame in groupDescriptionFrameList:
            if groupDescriptionFrame.isEnabled():
                groupNameList.append(groupDescriptionFrame.groupName)

        jsonHelper.addMachineToJSON(fileName,groupNameList)

        subprocess.call('cp \"'+filePath+'\" ./machineConfig/', shell=True)
        self.parent.destroy()

    def applyFilterTypeButtonPressed(self, filePath, groupDescriptionFrameList, filterType):
        components = filePath.split('/')
        fileName = components[-1]

        groupNameList = []

        for groupDescriptionFrame in groupDescriptionFrameList:
            if groupDescriptionFrame.isEnabled():
                groupNameList.append(groupDescriptionFrame.groupName)

        jsonHelper.addFilterTypeToJSON(fileName,groupNameList,filterType)

        if filterType == 'Head':
            subprocess.call('cp \"'+filePath+'\" ./filterTypesConfig/headFilters/', shell=True)
        else:
            subprocess.call('cp \"'+filePath+'\" ./filterTypesConfig/jawFilters/', shell=True)

        self.parent.destroy()

    def applyModuleButtonPressed(self, filePath, groupDescriptionFrameList):
        components = filePath.split('/')
        fileName = components[-1]

        groupNameList = []

        for groupDescriptionFrame in groupDescriptionFrameList:
            if groupDescriptionFrame.isEnabled():
                groupNameList.append(groupDescriptionFrame.groupName)

        jsonHelper.addModuleToJSON(fileName,groupNameList)

        subprocess.call('cp \"'+filePath+'\" ./moduleConfig/', shell=True)
        self.parent.destroy()