from tkinter import *
from tkinter import Toplevel, RAISED, Button, TOP, X, NORMAL, DISABLED, S, N, E, W, SUNKEN, Label, OptionMenu, BOTH, messagebox
from tkinter.ttk import Notebook
from eguanaModel import EguanaModel
from egpopupSettings.filterTypeCheckboxFrame import FilterTypeCheckboxFrame
from egpopupSettings.filterFunctionCheckboxFrame import FilterFunctionCheckboxFrame
import subprocess
import os.path
import json
from tests.machineConfigTest import MachineConfigTest
from tests.filterTypesConfigTest import FilterTypesConfigTest
from egpopupSettings.editSettingsFrame import EditSettingsFrame
from egpopupSettings.deleteSettingsFrame import DeleteSettingsFrame
from helpers import jsonHelper
from egpopupSettings.groupDescriptionCheckboxFrame import GroupDescriptionCheckboxFrame
class SettingsPopup(Toplevel):

    def __init__(self,parent):
    
        Toplevel.__init__(self) 
        self.transient(parent)
        self.focus()

        sw = parent.winfo_screenwidth()
        sh = parent.winfo_screenheight()
        self.geometry('%dx%d+%d+%d' % (sw/2, sh/2, sw/4, sh/4))
        self.grab_set()
        self.title("Settings")

        self.modeNotebook = Notebook(self)
        self.modeNotebook.pack(fill=BOTH, expand=True)

        self.addFrame = Frame(self.modeNotebook)
        self.addFrame.pack(fill=BOTH, expand=True)

        self.editFrame = EditSettingsFrame(self.modeNotebook,self)
        self.editFrame.pack(fill=BOTH, expand=True)

        self.deleteFrame = DeleteSettingsFrame(self.modeNotebook,self)
        self.deleteFrame.pack(fill=BOTH, expand=True)

        self.modeNotebook.add(self.addFrame, text='Add')
        self.modeNotebook.add(self.editFrame, text='Edit')
        self.modeNotebook.add(self.deleteFrame, text='Delete')

        self.editFrame.setupFrame()

        dropList = ['Machine', 'Head Filter','Jaw Filter','Module']
        dropTitle = StringVar()
        dropTitle.set('Select Type')
        drop = OptionMenu(self.addFrame,dropTitle,*dropList, command=self.selectTypeCallback)
        drop.grid(row=1, column=0, columnspan=4, sticky='ew')
        
        self.currentValue = None

        self.addFrame.rowconfigure(0,weight=1)
        self.addFrame.rowconfigure(1,weight=1)
        self.addFrame.rowconfigure(2,weight=1)
        self.addFrame.rowconfigure(3,weight=1)
        self.addFrame.rowconfigure(4,weight=1)

        self.addFrame.columnconfigure(0,weight=1)
        self.addFrame.columnconfigure(1,weight=1)
        self.addFrame.columnconfigure(2,weight=1)
        self.addFrame.columnconfigure(3,weight=1)
        self.addFrame.wait_window(self)


    def selectTypeCallback(self, value):

        if value != self.currentValue:

            self.currentValue = value

            for i in range(2,self.addFrame.grid_size()[1]): 
                    for element in self.addFrame.grid_slaves(i,None):
                        element.grid_forget()

            if value == 'Machine':
                loadButton = Button(self.addFrame, text='Load config file', relief=RAISED, command=lambda:self.machineLoadButtonPressed(loadButton))
                loadButton.grid(row=2, column=0, columnspan=4, sticky=E+W)


            elif value == 'Head Filter':
                loadButton = Button(self.addFrame, text='Load config file', relief=RAISED, command=lambda:self.headFilterTypeLoadButtonPressed(loadButton))
                loadButton.grid(row=2, column=0, columnspan=4, sticky=E+W)

            elif value == 'Jaw Filter':
                loadButton = Button(self.addFrame, text='Load config file', relief=RAISED, command=lambda:self.jawFilterTypeLoadButtonPressed(loadButton))
                loadButton.grid(row=2, column=0, columnspan=4, sticky=E+W)


            else: #'module'
                loadButton = Button(self.addFrame, text='Load config file', relief=RAISED, command=lambda:self.moduleLoadButtonPressed(loadButton))
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

                    groupDesctiptionNotebook = Notebook(self.addFrame)
                    groupDesctiptionNotebook.grid(row=3, column=0,columnspan=4, sticky=E+W)
                    

                    tabNameList = jsonHelper.getAllGroups()
                    groupDescriptionFrameList = [];


                    for i in range(len(tabNameList)):

                        groupDescriptionFrame = GroupDescriptionCheckboxFrame(groupDesctiptionNotebook,tabNameList[i])
                        groupDescriptionFrameList.append(groupDescriptionFrame)
                        groupDescriptionFrame.pack(fill=BOTH, expand=True)
                        groupDesctiptionNotebook.add(groupDescriptionFrame, text=tabNameList[i])
                      
                    Button(self.addFrame,text='Apply & Close',relief=RAISED,command=lambda:self.applyMachineButtonPressed(filePath, groupDescriptionFrameList)).grid(row=4,column=1,columnspan=1,sticky=S+E)
                
                else:
                    messagebox.showinfo("Error", errorString)

            else:
                messagebox.showinfo("Error", "File already exists in machineConfig directory: " + fileName)



    def headFilterTypeLoadButtonPressed(self,loadButton):

        filePath = filedialog.askopenfilename()
        if filePath != '':
            components = filePath.split('/')
            fileName = components[-1]

            if os.path.isfile(os.getcwd()+'/filterTypesConfig/headFilters/'+fileName) == False:                
                # [isValid, errorString] = FilterTypesConfigTest(filePath).runTests()
                isValid = 1
                if isValid:
                    loadButton.config(text=filePath)
                    self.filterTypeLoadButtonPressed(filePath,'Head')
                else:

                    messagebox.showinfo("Error","")
            else:
                messagebox.showinfo("Error", "File already exists in directory: " + fileName)

    def jawFilterTypeLoadButtonPressed(self,loadButton):

        filePath = filedialog.askopenfilename()
        if filePath != '':
            components = filePath.split('/')
            fileName = components[-1]

            if os.path.isfile(os.getcwd()+'/filterTypesConfig/jawFilters/'+fileName) == False:                
                # [isValid, errorString] = FilterTypesConfigTest(filePath).runTests()
                isValid = 1
                if isValid:
                    loadButton.config(text=filePath)
                    self.filterTypeLoadButtonPressed(filePath,'Jaw')
                else:

                    messagebox.showinfo("Error","")
            else:
                messagebox.showinfo("Error", "File already exists in directory: " + fileName)


    def filterTypeLoadButtonPressed(self, filePath,filterType):

        
        groupDesctiptionNotebook = Notebook(self.addFrame)
        groupDesctiptionNotebook.grid(row=3, column=0,columnspan=4, sticky=E+W)
        

        tabNameList = jsonHelper.getAllGroups()
        groupDescriptionFrameList = [];


        for i in range(len(tabNameList)):

            groupDescriptionFrame = GroupDescriptionCheckboxFrame(groupDesctiptionNotebook,tabNameList[i])
            groupDescriptionFrameList.append(groupDescriptionFrame)
            groupDescriptionFrame.pack(fill=BOTH, expand=True)
            groupDesctiptionNotebook.add(groupDescriptionFrame, text=tabNameList[i])
          
        Button(self.addFrame,text='Apply & Close',relief=RAISED,command=lambda:self.applyFilterTypeButtonPressed(filePath, groupDescriptionFrameList, filterType)).grid(row=4,column=1,columnspan=1,sticky=S+E)

    def moduleLoadButtonPressed(self,loadButton):

        filePath = filedialog.askopenfilename(filetypes=[('Python file','*.py')])
        
        if filePath != '':

            components = filePath.split('/')
            fileName = components[-1]

            if os.path.isfile(os.getcwd()+'/moduleConfig/'+fileName) == False:

                # [isValid, errorString] = MachineConfigTest(filePath).runTests() //TODO
                isValid = 1

                if isValid:

                    loadButton.config(text=filePath)

                    groupDesctiptionNotebook = Notebook(self.addFrame)
                    groupDesctiptionNotebook.grid(row=3, column=0,columnspan=4, sticky=E+W)
                    

                    tabNameList = jsonHelper.getAllGroups()
                    groupDescriptionFrameList = [];


                    for i in range(len(tabNameList)):

                        groupDescriptionFrame = GroupDescriptionCheckboxFrame(groupDesctiptionNotebook,tabNameList[i])
                        groupDescriptionFrameList.append(groupDescriptionFrame)
                        groupDescriptionFrame.pack(fill=BOTH, expand=True)
                        groupDesctiptionNotebook.add(groupDescriptionFrame, text=tabNameList[i])
                      
                    Button(self.addFrame,text='Apply & Close',relief=RAISED,command=lambda:self.applyModuleButtonPressed(filePath, groupDescriptionFrameList)).grid(row=4,column=1,columnspan=1,sticky=S+E)
                
                else:
                    messagebox.showinfo("Error", errorString)

            else:
                messagebox.showinfo("Error", "File already exists in moduleConfig directory: " + fileName)


    def applyMachineButtonPressed(self,filePath, groupDescriptionFrameList):


        components = filePath.split('/')
        fileName = components[-1]

        groupNameList = []

        for groupDescriptionFrame in groupDescriptionFrameList:
            if groupDescriptionFrame.isEnabled():
                groupNameList.append(groupDescriptionFrame.groupName)

        jsonHelper.addMachineToJSON(fileName,groupNameList)

        subprocess.call('cp '+filePath+' ./machineConfig/', shell=True)
        self.destroy()

    
    def applyFilterTypeButtonPressed(self,filePath,groupDescriptionFrameList,filterType):

        components = filePath.split('/')
        fileName = components[-1]

        groupNameList = []

        for groupDescriptionFrame in groupDescriptionFrameList:
            if groupDescriptionFrame.isEnabled():
                groupNameList.append(groupDescriptionFrame.groupName)

        jsonHelper.addFilterTypeToJSON(fileName,groupNameList,filterType)

        if filterType == 'Head':
            subprocess.call('cp '+filePath+' ./filterTypesConfig/headFilters/', shell=True)
        else:
            subprocess.call('cp '+filePath+' ./filterTypesConfig/jawFilters/', shell=True)

        self.destroy()
   
    def applyModuleButtonPressed(self,filePath, groupDescriptionFrameList):


        components = filePath.split('/')
        fileName = components[-1]

        groupNameList = []

        for groupDescriptionFrame in groupDescriptionFrameList:
            if groupDescriptionFrame.isEnabled():
                groupNameList.append(groupDescriptionFrame.groupName)

        jsonHelper.addModuleToJSON(fileName,groupNameList)

        subprocess.call('cp '+filePath+' ./moduleConfig/', shell=True)
        self.destroy()



                