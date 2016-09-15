from tkinter import *
from eguanaModel import EguanaModel
from helpers.jsonHelper import getEnabledFilterFunctionsNameForMachineFilename as getEnabledFilterFunctionsNameForMachineFilename
from helpers.jsonHelper import getEnabledHeadFilterFunctionFileNamesForMachineAndFilterFunctionFileNames as getEnabledHeadFilterFunctionFileNamesForMachineAndFilterFunctionFileNames
from helpers.jsonHelper import getEnabledJawFilterFunctionFileNamesForMachineAndFilterFunctionFileNames as getEnabledJawFilterFunctionFileNamesForMachineAndFilterFunctionFileNames
from helpers.jsonHelper import getEnabledMachineNameForFilterFunctionFilename as getEnabledMachineNameForFilterFunctionFilename
from tkinter.ttk import Notebook

from egpopupSettings.filterTypeCheckboxFrameForEdit import FilterTypeCheckboxFrameForEdit

class EditSettingsFrame(Frame):
    def __init__(self,notebook):
        Frame.__init__(self,notebook)
        self.currentTypeValue = None
        self.currentMachineTypeValue = None
        self.currentFilterFunctionValue = None

    def setupFrame(self):
        dropList = ['Machine', 'Filter Function', 'Filter Type']
        dropTitle = StringVar()
        dropTitle.set('Select Type')
        drop = OptionMenu(self,dropTitle,*dropList, command=self.selectTypeCallback)
        drop.grid(row=1, column=0, columnspan=4, sticky='ew')



        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.rowconfigure(3,weight=1)
        self.rowconfigure(4,weight=1)

        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        self.columnconfigure(3,weight=1)



    def selectTypeCallback(self, value):

        if value != self.currentTypeValue:

            self.currentTypeValue = value

            for i in range(2,self.grid_size()[1]): 
                    for element in self.grid_slaves(i,None):
                        element.grid_forget()

            if value == 'Machine':
                machineNamesList = EguanaModel().getAllMachines()
                machineNameList = [EguanaModel().getMachineObjectFromMachineName(machineFileName).name for machineFileName in machineNamesList]

                dropMachineTitle = StringVar()
                dropMachineTitle.set('Select Machine')
                machineDropMenu = OptionMenu(self,dropMachineTitle,*machineNameList,command=self.machineSelectedFromOptionsMenu)
                machineDropMenu.grid(row=2, column=0, columnspan=4, sticky='ew')


            elif value == 'Filter Function':
                filterFunctionFilenameList = EguanaModel().getAllFilterFunctions()
                filterFunctionsObjectList = EguanaModel().getFilterFunctionObjectsFromFunctionNameArray(filterFunctionFilenameList)

                filterFunctionNameList = [ffObject.name for ffObject in filterFunctionsObjectList]

                dropFFTitle = StringVar()
                dropFFTitle.set('Select Filter Function')
                ffDropMenu = OptionMenu(self,dropFFTitle,*filterFunctionNameList,command=self.filterFunctionSelectedFromOptionsMenu)
                ffDropMenu.grid(row=2, column=0, columnspan=4, sticky='ew')

            else: #'Filter Type'
                headCheckButtonInt = IntVar()
                headCheckButtonInt.set(1)
                jawCheckButtonInt = IntVar()

                headCheckButton = Checkbutton(self, text='Head', variable=headCheckButtonInt, command=lambda:self.headCheckButtonPressed(headCheckButtonInt,jawCheckButtonInt)).grid(row=2, column=0, columnspan=1, sticky=N+E+W)
                jawCheckButton = Checkbutton(self, text='Jaw', variable=jawCheckButtonInt, command=lambda:self.jawCheckButtonPressed(headCheckButtonInt,jawCheckButtonInt)).grid(row=2, column=2, columnspan=1, sticky=N+E+W)

                self.setupHeadDropDown()

    def filterFunctionSelectedFromOptionsMenu(self,value):
        
        if value != self.currentFilterFunctionValue:

            self.currentFilterFunctionValue = value

            for i in range(3,self.grid_size()[1]): 
                for element in self.grid_slaves(i,None):
                    element.grid_forget()


        filterFunctionFilenameList = EguanaModel().getAllFilterFunctions()
        filterFunctionsObjectList = EguanaModel().getFilterFunctionObjectsFromFunctionNameArray(filterFunctionFilenameList)

        selectedFilterFunction = None

        for ffObject in filterFunctionsObjectList:

            if ffObject.name == value:
                selectedFilterFunction = ffObject
                break

        if selectedFilterFunction:
            self.setupSelectedFilterConfig(selectedFilterFunction)


    def setupSelectedFilterConfig(self,selectedFilterFunctionObject):

        machineNotebook = Notebook(self)
        machineNotebook.grid(row=3,column=0,columnspan=4,sticky=E+W)


        allMachineFilenameList = EguanaModel().getAllMachines()

        headList = EguanaModel().getAllHeadFilterTypes()
        headObjectList = EguanaModel().getFilterTypeObjectsFromTypeNameArray(headList,'Head')

        jawList = EguanaModel().getAllJawFilterTypes()
        jawObjectList = EguanaModel().getFilterTypeObjectsFromTypeNameArray(jawList,'Jaw')


        filterTypeFrameList = []
        enabledMachineNameList = getEnabledMachineNameForFilterFunctionFilename(selectedFilterFunctionObject.getFilename())


        for machineFilename in allMachineFilenameList:

            isEnabled = machineFilename in enabledMachineNameList

            enabledJawFilenameList = []
            enabledHeadFilenameList = []

            if isEnabled:

                enabledJawFilenameList = getEnabledJawFilterFunctionFileNamesForMachineAndFilterFunctionFileNames(machineFilename,selectedFilterFunctionObject.getFilename())
                enabledHeadFilenameList = getEnabledHeadFilterFunctionFileNamesForMachineAndFilterFunctionFileNames(machineFilename,selectedFilterFunctionObject.getFilename())

                filterTypeFrame = FilterTypeCheckboxFrameForEdit(machineNotebook,headObjectList,jawObjectList,isEnabled,enabledJawFilenameList,enabledHeadFilenameList)
                filterTypeFrameList.append(filterTypeFrame)
                filterTypeFrame.pack(fill=BOTH, expand=True)
                machineNotebook.add(filterTypeFrame, text=EguanaModel().getMachineObjectFromMachineName(machineFilename).name)


    def machineSelectedFromOptionsMenu(self,value):

        if value != self.currentMachineTypeValue:

            self.currentMachineTypeValue = value

            for i in range(3,self.grid_size()[1]): 
                for element in self.grid_slaves(i,None):
                    element.grid_forget()

            machineNamesList = EguanaModel().getAllMachines()

            selectedMachine = None

            for machineFileName in machineNamesList:
                if EguanaModel().getMachineObjectFromMachineName(machineFileName).name == value:
                    selectedMachine = EguanaModel().getMachineObjectFromMachineName(machineFileName)
                    break


            if selectedMachine:
                self.setupSelectedMachineConfig(selectedMachine)




    def setupSelectedMachineConfig(self,selectedMachine):

        filterFunctionNotebook = Notebook(self)
        filterFunctionNotebook.grid(row=3, column=0,columnspan=4, sticky=E+W)


        allFilterFunctionsFilenameList = EguanaModel().getAllFilterFunctions()
        headList = EguanaModel().getAllHeadFilterTypes()
        headObjectList = EguanaModel().getFilterTypeObjectsFromTypeNameArray(headList,'Head')

        jawList = EguanaModel().getAllJawFilterTypes()
        jawObjectList = EguanaModel().getFilterTypeObjectsFromTypeNameArray(jawList,'Jaw')


        filterTypeFrameList = []

        enabledFilterFunctionNameList = getEnabledFilterFunctionsNameForMachineFilename(selectedMachine.getFilename())


        for filterFunctionFilename in allFilterFunctionsFilenameList:

            isEnabled = filterFunctionFilename in enabledFilterFunctionNameList
            enabledJawFilenameList = []
            enabledHeadFilenameList = []

            if isEnabled:

                enabledJawFilenameList = getEnabledJawFilterFunctionFileNamesForMachineAndFilterFunctionFileNames(selectedMachine.getFilename(),filterFunctionFilename)
                enabledHeadFilenameList = getEnabledHeadFilterFunctionFileNamesForMachineAndFilterFunctionFileNames(selectedMachine.getFilename(),filterFunctionFilename)


            filterTypeFrame = FilterTypeCheckboxFrameForEdit(filterFunctionNotebook,headObjectList,jawObjectList,isEnabled,enabledJawFilenameList,enabledHeadFilenameList)
            filterTypeFrameList.append(filterTypeFrame)
            filterTypeFrame.pack(fill=BOTH, expand=True)
            filterFunctionNotebook.add(filterTypeFrame, text=EguanaModel().getFilterObjectFromFunctionName(filterFunctionFilename).name)


    def headCheckButtonPressed(self,headCheckButtonInt,jawCheckButtonInt):

        if headCheckButtonInt.get():
            jawCheckButtonInt.set(0)
        else:
            jawCheckButtonInt.set(1)


        for i in range(3,self.grid_size()[1]): 
            for element in self.grid_slaves(i,None):
                element.grid_forget()


        if headCheckButtonInt.get():
            self.setupHeadDropDown()
        else:
            self.setupJawDropDown()


    def jawCheckButtonPressed(self,headCheckButtonInt,jawCheckButtonInt):
       
        if jawCheckButtonInt.get():
            headCheckButtonInt.set(0)
        else:
            headCheckButtonInt.set(1)

        for i in range(3,self.grid_size()[1]): 
            for element in self.grid_slaves(i,None):
                element.grid_forget()


        if headCheckButtonInt.get():
            self.setupHeadDropDown()
        else:
            self.setupJawDropDown()


    def setupHeadDropDown(self):
        headFilterTypeFilenameList = EguanaModel().getAllHeadFilterTypes()
        headFilterTypeObjectList = EguanaModel().getFilterTypeObjectsFromTypeNameArray(headFilterTypeFilenameList,'Head')

        headFilterTypeNamelist = [ftObject.name for ftObject in headFilterTypeObjectList]

        dropFtTitle = StringVar()
        dropFtTitle.set('Select Head Filter Type')
        ftDropMenu = OptionMenu(self,dropFtTitle,*headFilterTypeNamelist,command=self.filterTypeSelectedFromOptionsMenu)
        ftDropMenu.grid(row=3, column=0, columnspan=4, sticky='ew')

    def setupJawDropDown(self):

        jawFilterTypeFilenameList = EguanaModel().getAllJawFilterTypes()
        jawFilterTypeObjectList = EguanaModel().getFilterTypeObjectsFromTypeNameArray(jawFilterTypeFilenameList,'Jaw')

        jawFilterTypeNamelist = [ftObject.name for ftObject in jawFilterTypeObjectList]

        dropFtTitle = StringVar()
        dropFtTitle.set('Select Jaw Filter Type')
        ftDropMenu = OptionMenu(self,dropFtTitle,*jawFilterTypeNamelist,command=self.filterTypeSelectedFromOptionsMenu)
        ftDropMenu.grid(row=3, column=0, columnspan=4, sticky='ew')


    def filterTypeSelectedFromOptionsMenu(self):
        return

