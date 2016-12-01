from tkinter import *
from eguanaModel import EguanaModel
from egpopupSettings.groupDescriptionCheckboxFrame import GroupDescriptionCheckboxFrame

from helpers import jsonHelper

from helpers.jsonHelper import removeFilterTypeFromJSONForFilterType as removeFilterTypeFromJSONForFilterType
from helpers.jsonHelper import addFilterTypeToJSON as addFilterTypeToJSON
from helpers import jsonHelper
from helpers import objectHelper

from tkinter.ttk import Notebook


class EditSettingsFrame(Frame):
    def __init__(self,notebook,parent):
        Frame.__init__(self,notebook)
        self.currentTypeValue = None
        self.currentMachineTypeValue = None
        self.currentJawFilterTypeValue = None
        self.currentHeadFilterTypeValue = None
        self.currentModuleValue = None

        self.parent = parent

    def setupFrame(self):
        dropList = ['Machine', 'Head Filter','Jaw Filter','Module']
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

            for i in range(1,self.grid_size()[1]): 
                    for element in self.grid_slaves(i,None):
                        element.grid_forget()

            if value == 'Machine':
                self.setupMachineDropdown()           
            elif value == 'Head Filter':
                self.setupHeadDropDown()
            elif value == 'Jaw Filter':
                self.setupJawDropDown()
            else: #'Module'
                self.setupModuleDropdown()


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


    def setupSelectedMachineConfig(self,selectedMachineFilename):

        groupDesctiptionNotebook = Notebook(self)
        groupDesctiptionNotebook.grid(row=3, column=0, columnspan=4, sticky=E+W)
        

        tabNameList = jsonHelper.getAllGroups()
        groupDescriptionFrameList = [];

        groupNameList = jsonHelper.getAllGroupsForMachineFilename(selectedMachineFilename)

        for tabName in tabNameList:
            groupDescriptionFrame = GroupDescriptionCheckboxFrame(groupDesctiptionNotebook, tabName)
            isEnabled = tabName in groupNameList
            groupDescriptionFrame.enableCheckButtonInt.set(isEnabled)
            groupDescriptionFrameList.append(groupDescriptionFrame)
            groupDescriptionFrame.pack(fill=BOTH, expand=True)
            groupDesctiptionNotebook.add(groupDescriptionFrame, text=tabName)
          
        Button(self,text='Apply & Close',relief=RAISED,command=lambda:self.applyMachineButtonPressed(selectedMachineFilename,groupDescriptionFrameList)).grid(row=4,column=1,columnspan=1,sticky=S+E)

    def applyMachineButtonPressed(self, selectedMachineFileName, groupDescriptionFrameList):


        enabledGroupNames = []

        for groupDescriptionFrame in groupDescriptionFrameList:
            if groupDescriptionFrame.isEnabled():
                enabledGroupNames.append(groupDescriptionFrame.groupName)

        jsonHelper.removeMachineFromJSONForMachine(selectedMachineFileName)
        jsonHelper.addMachineToJSON(selectedMachineFileName,enabledGroupNames)

        self.parent.destroy()



    def setupMachineDropdown(self):
        machinefileNamesList = jsonHelper.getAllMachineFileNames()
        machineNameList = [objectHelper.getMachineNameFromMachineFilename(machineFilename) for machineFilename in machinefileNamesList]
        dropMachineTitle = StringVar()
        dropMachineTitle.set('Select Machine')
        machineDropMenu = OptionMenu(self,dropMachineTitle,*machineNameList,command=self.machineSelectedFromOptionsMenu)
        machineDropMenu.grid(row=1, column=0, columnspan=4, sticky='ew')


    def setupModuleDropdown(self):
        modulefileNamesList = jsonHelper.getAllModulesFileNames()
        moduleNamesList = [objectHelper.getModuleNameFromModuleFilename(moduleFilename) for moduleFilename in modulefileNamesList]
        dropModuleTitle = StringVar()
        dropModuleTitle.set('Select Module')
        moduleDropMenu = OptionMenu(self,dropModuleTitle,*moduleNamesList,command=self.moduleSelectedFromOptionsMenu)
        moduleDropMenu.grid(row=1, column=0, columnspan=4, sticky='ew')


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


    def setupSelectedModuleConfig(self,selectedModuleFileName):

        groupDesctiptionNotebook = Notebook(self)
        groupDesctiptionNotebook.grid(row=3, column=0, columnspan=4, sticky=E+W) 

        groupNameList = jsonHelper.getAllGroups()

        groupDescriptionFrameList = [];

        for groupName in groupNameList:
            groupDescriptionFrame = GroupDescriptionCheckboxFrame(groupDesctiptionNotebook, groupName)
            
            modulesForGroupList = jsonHelper.getModuleListForGroup(groupName)
            isEnabled = selectedModuleFileName in modulesForGroupList
            groupDescriptionFrame.enableCheckButtonInt.set(isEnabled)

            groupDescriptionFrameList.append(groupDescriptionFrame)
            groupDescriptionFrame.pack(fill=BOTH, expand=True)
            groupDesctiptionNotebook.add(groupDescriptionFrame, text=groupName)

        Button(self,text='Apply & Close',relief=RAISED,command=lambda:self.applyModuleButtonPressed(selectedModuleFileName,groupDescriptionFrameList)).grid(row=4,column=1,columnspan=1,sticky=S+E)


    def setupSelectedFilterType(self,selectedFilterFileName,filterType):

        groupDesctiptionNotebook = Notebook(self)
        groupDesctiptionNotebook.grid(row=3, column=0, columnspan=4, sticky=E+W) 

        groupNameList = jsonHelper.getAllGroups()

        groupDescriptionFrameList = [];

        for groupName in groupNameList:
            groupDescriptionFrame = GroupDescriptionCheckboxFrame(groupDesctiptionNotebook, groupName)
            #get selected filters for groupname
            selectedFilterList = []

            if filterType == 'Head':
                selectedFilterList = jsonHelper.getHeadFiltersListForGroup(groupName)
            else:
                selectedFilterList = jsonHelper.getJawFiltersListForGroup(groupName)

            isEnabled = selectedFilterFileName in selectedFilterList
            groupDescriptionFrame.enableCheckButtonInt.set(isEnabled)
            groupDescriptionFrameList.append(groupDescriptionFrame)
            groupDescriptionFrame.pack(fill=BOTH, expand=True)
            groupDesctiptionNotebook.add(groupDescriptionFrame, text=groupName)

        Button(self,text='Apply & Close',relief=RAISED,command=lambda:self.applyFilterTypeButtonPressed(selectedFilterFileName,groupDescriptionFrameList,filterType)).grid(row=4,column=1,columnspan=1,sticky=S+E)


    def applyFilterTypeButtonPressed(self,selectedFilterFileName,groupDescriptionFrameList,filterType):


        enabledGroupNames = []

        for groupDescriptionFrame in groupDescriptionFrameList:
            if groupDescriptionFrame.isEnabled():
                enabledGroupNames.append(groupDescriptionFrame.groupName)

        jsonHelper.removeFilterTypeFromJSONForFilterType(selectedFilterFileName,filterType)
        jsonHelper.addFilterTypeToJSON(selectedFilterFileName,enabledGroupNames,filterType)
        
        self.parent.destroy()          


    def applyModuleButtonPressed(self,selectedModuleFileName,groupDescriptionFrameList):

        enabledGroupNames = []

        for groupDescriptionFrame in groupDescriptionFrameList:
            if groupDescriptionFrame.isEnabled():
                enabledGroupNames.append(groupDescriptionFrame.groupName)


        jsonHelper.removeModuleFromJSON(selectedModuleFileName)
        jsonHelper.addModuleToJSON(selectedModuleFileName,enabledGroupNames)
        
        self.parent.destroy()     





