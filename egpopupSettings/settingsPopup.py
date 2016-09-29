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
from tests.filterConfigTest import FilterConfigTest
from tests.filterTypesConfigTest import FilterTypesConfigTest
from egpopupSettings.editSettingsFrame import EditSettingsFrame
from egpopupSettings.deleteSettingsFrame import DeleteSettingsFrame

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

        dropList = ['Machine', 'Filter Function', 'Filter Type']
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


            elif value == 'Filter Function':
                loadButton = Button(self.addFrame, text='Load config file', relief=RAISED, command=lambda:self.filterFunctionLoadButtonPressed(loadButton))
                loadButton.grid(row=2, column=0, columnspan=4, sticky=E+W)


            else: #'Filter Type'
                loadButton = Button(self.addFrame, text='Load config file', relief=RAISED, command=lambda:self.filterTypeLoadButtonPressed(loadButton))
                loadButton.grid(row=2, column=0, columnspan=4, sticky=E+W)



    def machineLoadButtonPressed(self, loadButton):

        filePath = filedialog.askopenfilename(filetypes=[('Python file','*.py')])
        
        if filePath != '':

            components = filePath.split('/')
            fileName = components[-1]

            if os.path.isfile(os.getcwd()+'/machineConfig/'+fileName) == False:


                [isValid, errorString] = MachineConfigTest(filePath).runTests()

                if isValid:

                    loadButton.config(text=filePath)

                    filterFunctionNotebook = Notebook(self.addFrame)
                    filterFunctionNotebook.grid(row=3, column=0,columnspan=4, sticky=E+W)
                    
                    dropList = EguanaModel().getAllFilterFunctions()

                    headList = EguanaModel().getAllHeadFilterTypes()
                    modifiedHeadList = EguanaModel().getFilterTypeObjectsFromTypeNameArray(headList,'Head') # TODO : rename to headObjectList when refactor

                    jawList = EguanaModel().getAllJawFilterTypes()
                    modifiedJawList = EguanaModel().getFilterTypeObjectsFromTypeNameArray(jawList,'Jaw')
                

                    filterTypeFrameList = []

                    for i in range(len(dropList)):

                        filterTypeFrame = FilterTypeCheckboxFrame(filterFunctionNotebook,modifiedHeadList,modifiedJawList)
                        filterTypeFrameList.append(filterTypeFrame)
                        filterTypeFrame.pack(fill=BOTH, expand=True)
                        filterFunctionNotebook.add(filterTypeFrame, text=EguanaModel().getFilterObjectFromFunctionName(dropList[i]).name)
                      
                    applyButton  = Button(self.addFrame,text='Apply & Close',relief=RAISED,command=lambda:self.applyMachineButtonPressed(filePath, dropList, filterTypeFrameList)).grid(row=4,column=1,columnspan=1,sticky=S+E)
                
                else:
                    messagebox.showinfo("Error", errorString)

            else:
                messagebox.showinfo("Error", "File already exists in machineConfig directory: " + fileName)




    def filterFunctionLoadButtonPressed(self, loadButton):

        filePath = filedialog.askopenfilename()
            
        if filePath != '':

            components = filePath.split('/')
            fileName = components[-1]


            if os.path.isfile(os.getcwd()+'/filterConfig/'+fileName) == False:

                [isValid, errorString] = FilterConfigTest(filePath).runTests()

                if isValid:

                    loadButton.config(text=filePath)

                    filterFunctionNotebook = Notebook(self.addFrame)
                    filterFunctionNotebook.grid(row=3, column=0,columnspan=4, sticky=E+W)

                    dropList = EguanaModel().getAllMachines()

                    headList = EguanaModel().getAllHeadFilterTypes()
                    modifiedHeadList = EguanaModel().getFilterTypeObjectsFromTypeNameArray(headList,'Head')

                    jawList = EguanaModel().getAllJawFilterTypes()
                    modifiedJawList = EguanaModel().getFilterTypeObjectsFromTypeNameArray(jawList,'Jaw')
                
                    filterTypeFrameList = []

                    for i in range(len(dropList)):

                        filterTypeFrame = FilterTypeCheckboxFrame(filterFunctionNotebook,modifiedHeadList,modifiedJawList)
                        filterTypeFrame.pack(fill=BOTH, expand=True)
                        filterFunctionNotebook.add(filterTypeFrame, text=EguanaModel().getMachineObjectFromMachineName(dropList[i]).name)
                        filterTypeFrameList.append(filterTypeFrame)

                    applyButton  = Button(self.addFrame,text='Apply & Close',relief=RAISED,command=lambda:self.applyFilterFunctionButtonPressed(filePath,dropList,filterTypeFrameList)).grid(row=4,column=1,columnspan=1,sticky=S+E)

                else:
                    messagebox.showinfo("Error",errorString)
            else:
                messagebox.showinfo("Error", "File already exists in machineConfig directory: " + fileName)


    def filterTypeLoadButtonPressed(self, loadButton):

        filePath = filedialog.askopenfilename()
            
        if filePath != '':

            components = filePath.split('/')
            fileName = components[-1]

            if os.path.isfile(os.getcwd()+'/filterTypesConfig/headFilters/'+fileName) == False \
                and os.path.isfile(os.getcwd()+'/filterTypesConfig/jawFilters/'+fileName) == False:            
                
                # [isValid, errorString] = FilterTypesConfigTest(filePath).runTests()
                isValid = 1

                if isValid:

                    loadButton.config(text=filePath)

                    headCheckButtonInt = IntVar()
                    headCheckButtonInt.set(1)
                    jawCheckButtonInt = IntVar()

                    headCheckButton = Checkbutton(self.addFrame, text='Head', variable=headCheckButtonInt, command=lambda:self.headCheckButtonPressed(headCheckButtonInt,jawCheckButtonInt)).grid(row=3, column=0, columnspan=1, sticky=N+E+W)
                    jawCheckButton = Checkbutton(self.addFrame, text='Jaw', variable=jawCheckButtonInt, command=lambda:self.jawCheckButtonPressed(headCheckButtonInt,jawCheckButtonInt)).grid(row=3, column=2, columnspan=1, sticky=N+E+W)


                    filterFunctionNotebook = Notebook(self.addFrame)
                    filterFunctionNotebook.grid(row=4, column=0,columnspan=4, sticky=E+W)

                    dropList = EguanaModel().getAllMachines()

                    filterFunctionNameList = EguanaModel().getAllFilterFunctions()
                    filterFunctionObjectList = EguanaModel().getFilterFunctionObjectsFromFunctionNameArray(filterFunctionNameList)

                    filterFunctionFrameList = []

                    for i in range(len(dropList)):

                        filterFunctionFrame = FilterFunctionCheckboxFrame(filterFunctionNotebook,filterFunctionObjectList)
                        filterFunctionFrame.pack(fill=BOTH, expand=True)
                        filterFunctionNotebook.add(filterFunctionFrame, text=EguanaModel().getMachineObjectFromMachineName(dropList[i]).name)
                        filterFunctionFrameList.append(filterFunctionFrame)

                    applyButton  = Button(self.addFrame,text='Apply & Close',relief=RAISED,command=lambda:self.applyFilterTypeButtonPressed(filePath,headCheckButtonInt,jawCheckButtonInt,dropList,filterFunctionFrameList)).grid(row=5,column=1,columnspan=1,sticky=S+E)

                else:

                    messagebox.showinfo("Error",errorString)

            else:
                messagebox.showinfo("Error", "File already exists in machineConfig directory: " + fileName)

    
    def applyMachineButtonPressed(self,filePath, dropList, filterTypeFrameList):

        with open("./config.json", 'r') as f:
            configJSONDict = json.loads(f.read())

        configArray = configJSONDict["configurations"]

        newMachineDict = {}

        components = filePath.split('/')
        fileName = components[-1]
        newMachineDict["machineName"] = fileName

        newFilterFunctionsList = []

        for i in range(len(filterTypeFrameList)):
            if filterTypeFrameList[i].isEnabled():
                newFilterFunctionDict = {}
                newFilterFunctionDict["filterApplicationName"] =  EguanaModel().getFilterObjectFromFunctionName(dropList[i]).name

                filterTypesDict = {}

                filterTypesDict['headFilters'] = filterTypeFrameList[i].getEnabledHeadFilterTypeNames()
                filterTypesDict['jawFilters'] = filterTypeFrameList[i].getEnabledJawFilterTypeNames()

                newFilterFunctionDict['filterTypes'] = filterTypesDict
                newFilterFunctionsList.append(newFilterFunctionDict)

        newMachineDict['filterFunctions'] = newFilterFunctionsList
        configArray.append(newMachineDict)

        allMachinesList = configJSONDict["allMachines"]
        allMachinesList.append(fileName)


        with open("./config.json", 'w') as f:
            json.dump(configJSONDict,f)

        subprocess.call('cp '+filePath+' ./machineConfig/', shell=True)
        self.destroy()

    def applyFilterFunctionButtonPressed(self,filePath, dropList, filterTypeFrameList):


        components = filePath.split('/')
        fileName = components[-1]

        with open("./config.json", 'r') as f:
            configJSONDict = json.loads(f.read())

        configArray = configJSONDict["configurations"]


        for machineDict in configArray:

            if filterTypeFrameList[dropList.index(machineDict['machineName'])].isEnabled():

                newFilterFunctionDict = {}
                newFilterFunctionDict['filterApplicationName'] = fileName

                filterTypesDict = {}
                filterTypesDict['headFilters'] = filterTypeFrameList[dropList.index(machineDict['machineName'])].getEnabledHeadFilterTypeNames()
                filterTypesDict['jawFilters'] = filterTypeFrameList[dropList.index(machineDict['machineName'])].getEnabledJawFilterTypeNames()

                newFilterFunctionDict['filterTypes'] = filterTypesDict

                filterFunctionsArray = machineDict['filterFunctions']
                filterFunctionsArray.append(newFilterFunctionDict)


        allFilterFuctions = configJSONDict["allFilterFunctions"]
        allFilterFuctions.append(fileName)


        with open("./config.json", 'w') as f:
            json.dump(configJSONDict,f)

        subprocess.call('cp '+filePath+' ./filterConfig/', shell=True)
        self.destroy()


    def applyFilterTypeButtonPressed(self,filePath,headCheckButtonInt,jawCheckButtonInt,dropList, filterFunctionFrameList):


        components = filePath.split('/')
        fileName = components[-1]

        with open("./config.json", 'r') as f:
            configJSONDict = json.loads(f.read())

        configArray = configJSONDict["configurations"]

        for machineDict in configArray:

            if filterFunctionFrameList[dropList.index(machineDict['machineName'])].isEnabled():

                enabledFilterFunctionFilenameList = filterFunctionFrameList[dropList.index(machineDict['machineName'])].getEnabledFilterFunctionNames()

                filterFunctionJsonList = machineDict['filterFunctions']


                for filterFunctionFilename in enabledFilterFunctionFilenameList:

                    filterFunctionTmpDictionary = None

                    for filterFunctionDict in filterFunctionJsonList:

                        if filterFunctionDict['filterApplicationName'] == filterFunctionFilename:

                            filterFunctionTmpDictionary = filterFunctionDict
                            break


                    if filterFunctionTmpDictionary:
                        if headCheckButtonInt.get():
                            filterTypeArray = filterFunctionTmpDictionary['filterTypes']['headFilters']
                            filterTypeArray.append(fileName)
                        else:
                            filterTypeArray = filterFunctionTmpDictionary['filterTypes']['jawFilter']
                            filterTypeArray.append(fileName)
                    else:

                        filterFunctionTmpDictionary = {}
                        filterFunctionTmpDictionary['headFilters'] = []
                        filterFunctionTmpDictionary['jawFilters'] = []
                        filterFunctionTmpDictionary['filterApplicationName'] = filterFunctionFilename

                        if headCheckButtonInt.get():
                            filterTypeArray = filterFunctionTmpDictionary['headFilters']
                            filterTypeArray.append(fileName)
                        else:
                            filterTypeArray = filterFunctionTmpDictionary['jawFilters']
                            filterTypeArray.append(fileName)

                        filterFunctionJsonList.append(filterFunctionTmpDictionary)







        if headCheckButtonInt.get():
            allHeadFilterTypes = configJSONDict["allHeadFilterTypes"]
            allHeadFilterTypes.append(fileName)
        else:
            allJawFilterTypes = configJSONDict['allJawFilterTypes']
            allJawFilterTypes.append(fileName)


        with open("./config.json", 'w') as f:
            json.dump(configJSONDict,f)



        if headCheckButtonInt.get():
            subprocess.call('cp '+filePath+' ./filterTypesConfig/headFilters/', shell=True)
        else:
            subprocess.call('cp '+filePath+' ./filterTypesConfig/jawFilters/', shell=True)

        self.destroy()

    def headCheckButtonPressed(self,headCheckButtonInt,jawCheckButtonInt):

        if headCheckButtonInt.get():
            jawCheckButtonInt.set(0)
        else:
            jawCheckButtonInt.set(1)



    def jawCheckButtonPressed(self,headCheckButtonInt,jawCheckButtonInt):
       
        if jawCheckButtonInt.get():
            headCheckButtonInt.set(0)
        else:
            headCheckButtonInt.set(1)



                