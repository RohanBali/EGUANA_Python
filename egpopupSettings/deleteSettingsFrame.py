from tkinter import *
from eguanaModel import EguanaModel
from helpers import jsonHelper
from helpers import objectHelper
from egpopupSettings.groupDescriptionCheckboxFrame import GroupDescriptionCheckboxFrame
from tkinter.ttk import Notebook
import os

class DeleteSettingsFrame(Frame):
    def __init__(self,notebook,parent):
        Frame.__init__(self,notebook)
        self.parent = parent
        self.currentTypeValue = None
        self.currentMachineTypeValue = None
        self.currentFilterFunctionValue = None
        self.currentHeadFilterTypeValue = None
        self.currentJawFilterTypeValue = None
        self.currentModuleValue = None
        self.currentGroupValue = None
        self.setupFrame()

    def setupFrame(self):
        dropList = ['Machine', 'Head Filter','Jaw Filter','Module','Group']
        dropTitle = StringVar()
        dropTitle.set('Select Type')
        drop = OptionMenu(self,dropTitle,*dropList, command=self.selectTypeCallback)
        drop.grid(row=0, column=0, columnspan=4, sticky='ew')
        
        for row in range(0, 5):
            self.rowconfigure(row, weight=1)

        for col in range(0, 4):
            self.columnconfigure(col, weight=1)



    def selectTypeCallback(self, value):
        
        if value != self.currentTypeValue:

            self.currentTypeValue = value

            self.eraseConfigValues()

            for i in range(1,self.grid_size()[1]): 
                    for element in self.grid_slaves(i,None):
                        element.grid_forget()

            if value == 'Machine':
                self.setupMachineDropdown()           
            elif value == 'Head Filter':
                self.setupHeadDropDown()
            elif value == 'Jaw Filter':
                self.setupJawDropDown()
            elif value == 'Module':
                self.setupModuleDropdown()
            else: #group
                self.setupGroup()

    def eraseConfigValues(self):

        self.currentMachineTypeValue = None
        self.currentFilterFunctionValue = None
        self.currentHeadFilterTypeValue = None
        self.currentJawFilterTypeValue = None
        self.currentModuleValue = None
        self.currentGroupValue = None

    def setupMachineDropdown(self):
        
        machinefileNamesList = jsonHelper.getAllMachineFileNames()
        machineNameList = [objectHelper.getMachineNameFromMachineFilename(machineFilename) for machineFilename in machinefileNamesList]
        dropMachineTitle = StringVar()
        dropMachineTitle.set('Select Machine')
        machineDropMenu = OptionMenu(self,dropMachineTitle,*machineNameList,command=self.machineSelectedFromOptionsMenu)
        machineDropMenu.grid(row=1, column=0, columnspan=4, sticky='ew')

    def setupHeadDropDown(self):

        headFilterTypeFilenameList = jsonHelper.getAllHeadFiltersFileNames()
        headFilterNameList = [objectHelper.getHeadFilterNameFromHeadFilterFilename(filename) for filename in headFilterTypeFilenameList]
        dropFtTitle = StringVar()
        dropFtTitle.set('Select Head Filter Type')
        ftDropMenu = OptionMenu(self,dropFtTitle,*headFilterNameList,command=self.headFilterTypeSelectedFromOptionsMenu)
        ftDropMenu.grid(row=1, column=0, columnspan=4, sticky='ew')

    def setupJawDropDown(self):

        jawFilterTypeFilenameList = jsonHelper.getAllJawFiltersFileNames()
        jawFilterNameList = [objectHelper.getJawFilterNameFromJawFilterFilename(filename) for filename in jawFilterTypeFilenameList]
        dropFtTitle = StringVar()
        dropFtTitle.set('Select Jaw Filter Type')
        ftDropMenu = OptionMenu(self,dropFtTitle,*jawFilterNameList,command=self.jawFilterTypeSelectedFromOptionsMenu)
        ftDropMenu.grid(row=1, column=0, columnspan=4, sticky='ew')
    
    def setupModuleDropdown(self):
        modulefileNamesList = jsonHelper.getAllModulesFileNames()
        moduleNamesList = [objectHelper.getModuleNameFromModuleFilename(moduleFilename) for moduleFilename in modulefileNamesList]
        dropModuleTitle = StringVar()
        dropModuleTitle.set('Select Module')
        moduleDropMenu = OptionMenu(self,dropModuleTitle,*moduleNamesList,command=self.moduleSelectedFromOptionsMenu)
        moduleDropMenu.grid(row=1, column=0, columnspan=4, sticky='ew')

    def setupGroup(self):
        groupNameList = jsonHelper.getAllGroups()
        dropGroupTitle = StringVar()
        dropGroupTitle.set('Select Group')
        groupDropMenu = OptionMenu(self,dropGroupTitle,*groupNameList,command=self.groupSelectedFromOptionsMenu)
        groupDropMenu.grid(row=1, column=0, columnspan=4, sticky='ew')        


    def machineSelectedFromOptionsMenu(self,value):

        if value != self.currentMachineTypeValue:

            self.currentMachineTypeValue = value

            for i in range(2,self.grid_size()[1]): 
                for element in self.grid_slaves(i,None):
                    element.grid_forget()

            machineFilenamesList =  jsonHelper.getAllMachineFileNames()

            selectedMachineFilename = None

            for machineFileName in machineFilenamesList:
                if objectHelper.getMachineNameFromMachineFilename(machineFileName) == value:
                    selectedMachineFilename = machineFileName

            if selectedMachineFilename:
                self.setupSelectedMachineConfig(selectedMachineFilename)

    def groupSelectedFromOptionsMenu(self,value):

        if value != self.currentGroupValue:

            self.currentGroupValue = value

            for i in range(2,self.grid_size()[1]): 
                for element in self.grid_slaves(i,None):
                    element.grid_forget()

            self.setupSelectedGroupConfig(value)

    def moduleSelectedFromOptionsMenu(self,value):

        if value != self.currentModuleValue:

            self.currentModuleValue = value

            for i in range(2,self.grid_size()[1]): 
                for element in self.grid_slaves(i,None):
                    element.grid_forget()

            moduleFileNamesList =  jsonHelper.getAllModulesFileNames()

            selectedModuleFileName = None

            for moduleFileName in moduleFileNamesList:
                if objectHelper.getModuleNameFromModuleFilename(moduleFileName) == value:
                    selectedModuleFileName = moduleFileName

            if selectedModuleFileName:
                self.setupSelectedModuleConfig(selectedModuleFileName)


    def jawFilterTypeSelectedFromOptionsMenu(self,value):

        if value != self.currentJawFilterTypeValue:
            self.currentFilterFunctionValue = value

            for i in range(2,self.grid_size()[1]): 
                for element in self.grid_slaves(i,None):
                    element.grid_forget()


            jawFileNameList = jsonHelper.getAllJawFiltersFileNames()

            selectedJawFileName = None

            for jawFileName in jawFileNameList:
                if objectHelper.getJawFilterNameFromJawFilterFilename(jawFileName) == value:
                    selectedJawFileName = jawFileName
                    break

            if selectedJawFileName:
                self.setupSelectedFilterType(selectedJawFileName,'Jaw')


    def headFilterTypeSelectedFromOptionsMenu(self,value):

        if value != self.currentHeadFilterTypeValue:
            self.currentHeadFilterTypeValue = value

            for i in range(2,self.grid_size()[1]): 
                for element in self.grid_slaves(i,None):
                    element.grid_forget()


            headFileNameList = jsonHelper.getAllHeadFiltersFileNames()

            selectedHeadFileName = None

            for headFileName in headFileNameList:
                if objectHelper.getHeadFilterNameFromHeadFilterFilename(headFileName) == value:
                    selectedHeadFileName = headFileName
                    break

            if selectedHeadFileName:
                self.setupSelectedFilterType(selectedHeadFileName,'Head')


    def setupSelectedGroupConfig(self,groupName):

        Button(self,text='Delete & Close',relief=RAISED,command=lambda:self.deleteGroupButtonPressed(groupName)).grid(row=3,column=1,columnspan=1,sticky=S+E)

    def setupSelectedMachineConfig(self,selectedMachineFilename):

        Button(self,text='Delete & Close',relief=RAISED,command=lambda:self.deleteMachineButtonPressed(selectedMachineFilename)).grid(row=3,column=1,columnspan=1,sticky=S+E)

    def setupSelectedFilterType(self,selectedFilterFileName,filterType):

        Button(self,text='Delete & Close',relief=RAISED,command=lambda:self.deleteFilterTypeButtonPressed(selectedFilterFileName,filterType)).grid(row=4,column=1,columnspan=1,sticky=S+E)

    def setupSelectedModuleConfig(self,selectedModuleFileName):

        Button(self,text='Delete & Close',relief=RAISED,command=lambda:self.deleteModuleButtonPressed(selectedModuleFileName)).grid(row=4,column=1,columnspan=1,sticky=S+E)


    def deleteGroupButtonPressed(self, groupName):
        
        jsonHelper.removeGroupFromJSON(groupName)
        self.parent.destroy()

    def deleteMachineButtonPressed(self, selectedMachineFileName):
        
        jsonHelper.removeMachineFromJSONForMachine(selectedMachineFileName)
        os.remove('./machineConfig/'+selectedMachineFileName)    
        self.parent.destroy()

    def deleteFilterTypeButtonPressed(self,selectedFilterFileName,filterType):

        jsonHelper.removeFilterTypeFromJSONForFilterType(selectedFilterFileName,filterType)

        if filterType ==  'Head':
            os.remove('./filterTypesConfig/headFilters/'+selectedFilterFileName)    
        else:
            os.remove('./filterTypesConfig/jawFilters/'+selectedFilterFileName)  

        self.parent.destroy()     


    def deleteModuleButtonPressed(self,selectedModuleFileName):

        jsonHelper.removeModuleFromJSON(selectedModuleFileName)
        os.remove('./moduleConfig/'+selectedModuleFileName)    

        self.parent.destroy()



