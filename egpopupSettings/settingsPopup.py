from tkinter import *
from tkinter import Toplevel, RAISED, Button, TOP, X, NORMAL, DISABLED, S, N, E, W, SUNKEN, Label, OptionMenu, BOTH, messagebox
from tkinter.ttk import Notebook
from eguanaModel import EguanaModel
from egpopupSettings.filterTypeCheckboxFrame import FilterTypeCheckboxFrame
from egpopupSettings.filterFunctionCheckboxFrame import FilterFunctionCheckboxFrame
import subprocess
import os.path
import json

class SettingsPopup(Toplevel):

    def __init__(self,parent):
    
        Toplevel.__init__(self) 
        self.transient(parent)
        self.focus()

        sw = parent.winfo_screenwidth()
        sh = parent.winfo_screenheight()
        self.geometry('%dx%d+%d+%d' % (sw/4, sh/4, sw/2-sw/8, sh/2-sh/8))
        self.grab_set()
        self.title("Settings")

        self.modeNotebook = Notebook(self)
        self.modeNotebook.pack(fill=BOTH, expand=True)

        self.addFrame = Frame(self.modeNotebook)
        self.addFrame.pack(fill=BOTH, expand=True)

        self.editFrame = Frame(self.modeNotebook)
        self.editFrame.pack(fill=BOTH, expand=True)

        self.modeNotebook.add(self.addFrame, text='Add')
        self.modeNotebook.add(self.editFrame, text='Edit')
         
                
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

            for i in range(3,self.addFrame.grid_size()[1]): 
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

        filePath = filedialog.askopenfilename()
        
        if filePath != '':

            components = filePath.split('/')
            fileName = components[-1]

            if os.path.isfile(os.getcwd()+'/machineConfig/'+fileName) == False:

                loadButton.config(text=filePath)

                filterFunctionNotebook = Notebook(self.addFrame)
                filterFunctionNotebook.grid(row=3, column=0,columnspan=4, sticky=E+W)
                
                dropList = EguanaModel().getAllFilterFunctions()

                headList = EguanaModel().getAllHeadFilterTypes()
                modifiedHeadList = EguanaModel().getFilterTypeObjectsFromTypeNameArray(headList,'Head')

                jawList = EguanaModel().getAllJawFilterTypes()
                modifiedJawList = EguanaModel().getFilterTypeObjectsFromTypeNameArray(jawList,'Jaw')
            

                filterFunctionFrameList = []

                for i in range(len(dropList)):

                    filterFunctionFrame = FilterTypeCheckboxFrame(filterFunctionNotebook,modifiedHeadList,modifiedJawList)
                    filterFunctionFrameList.append(filterFunctionFrame)
                    filterFunctionFrame.pack(fill=BOTH, expand=True)
                    filterFunctionNotebook.add(filterFunctionFrame, text=EguanaModel().getFilterObjectFromFunctionName(dropList[i]).name)
                  
                applyButton  = Button(self.addFrame,text='Apply & Close',relief=RAISED,command=lambda:self.applyMachineButtonPressed(filePath, dropList, filterFunctionFrameList)).grid(row=4,column=3,columnspan=1,sticky=S+E)
            
            else:
                messagebox.showinfo("Error", "File already exists in machineConfig directory: " + fileName)




    def filterFunctionLoadButtonPressed(self, loadButton):

        filePath = filedialog.askopenfilename()
            
        if filePath != '':

            components = filePath.split('/')
            fileName = components[-1]


            if os.path.isfile(os.getcwd()+'/filterConfig/'+fileName) == False:

                loadButton.config(text=filePath)

                filterFunctionNotebook = Notebook(self.addFrame)
                filterFunctionNotebook.grid(row=3, column=0,columnspan=4, sticky=E+W)

                dropList = EguanaModel().getAllMachines()

                headList = EguanaModel().getAllHeadFilterTypes()
                modifiedHeadList = EguanaModel().getFilterTypeObjectsFromTypeNameArray(headList,'Head')

                jawList = EguanaModel().getAllJawFilterTypes()
                modifiedJawList = EguanaModel().getFilterTypeObjectsFromTypeNameArray(jawList,'Jaw')
            
                for i in range(len(dropList)):

                    filterFunctionFrame = FilterTypeCheckboxFrame(filterFunctionNotebook,modifiedHeadList,modifiedJawList)
                    filterFunctionFrame.pack(fill=BOTH, expand=True)
                    filterFunctionNotebook.add(filterFunctionFrame, text=EguanaModel().getMachineObjectFromMachineName(dropList[i]).name)
        
                applyButton  = Button(self.addFrame,text='Apply & Close',relief=RAISED,command=lambda:self.applyFilterFunctionButtonPressed(filePath)).grid(row=4,column=3,columnspan=1,sticky=S+E)

            else:
                messagebox.showinfo("Error", "File already exists in machineConfig directory: " + fileName)


    def filterTypeLoadButtonPressed(self, loadButton):

        filePath = filedialog.askopenfilename()
            
        if filePath != '':

            components = filePath.split('/')
            fileName = components[-1]


            if os.path.isfile(os.getcwd()+'/filterTypesConfig/headFilters/'+fileName) == False \
                and os.path.isfile(os.getcwd()+'/filterTypesConfig/jawFilters/'+fileName) == False:            

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


                for i in range(len(dropList)):

                    filterFunctionFrame = FilterFunctionCheckboxFrame(filterFunctionNotebook,filterFunctionObjectList)
                    filterFunctionFrame.pack(fill=BOTH, expand=True)
                    filterFunctionNotebook.add(filterFunctionFrame, text=EguanaModel().getMachineObjectFromMachineName(dropList[i]).name)
     
                applyButton  = Button(self.addFrame,text='Apply & Close',relief=RAISED,command=lambda:self.applyFilterTypeButtonPressed(filePath,headCheckButtonInt,jawCheckButtonInt)).grid(row=5,column=3,columnspan=1,sticky=S+E)

            else:
                messagebox.showinfo("Error", "File already exists in machineConfig directory: " + fileName)

    
    def applyMachineButtonPressed(self,filePath, dropList, filterFunctionFrameList):

        with open("./config.json", 'r') as f:
            configJSONDict = json.loads(f.read())

        configArray = configJSONDict["configurations"]

        newMachineDict = {}

        components = filePath.split('/')
        fileName = components[-1]
        newMachineDict["machineName"] = fileName

        newFilterFunctionsList = []

        for i in range(len(filterFunctionFrameList)):
            if filterFunctionFrameList[i].isEnabled():
                newFilterFunctionDict = {}
                newFilterFunctionDict["filterApplicationName"] =  EguanaModel().getFilterObjectFromFunctionName(dropList[i]).name

                filterTypesDict = {}

                filterTypesDict['headFilters'] = filterFunctionFrameList[i].getEnabledHeadFilterTypeNames()
                filterTypesDict['jawFilters'] = filterFunctionFrameList[i].getEnabledJawFilterTypeNames()

                newFilterFunctionDict['filterTypes'] = filterTypesDict
                newFilterFunctionsList.append(newFilterFunctionDict)

        newMachineDict['filterFunctions'] = newFilterFunctionsList

        configArray.append(newMachineDict)

        with open("./config.json", 'w') as f:
            json.dump(configJSONDict,f)

        subprocess.call('cp '+filePath+' ./machineConfig/', shell=True)
        self.destroy()

    def applyFilterFunctionButtonPressed(self,filePath):
        subprocess.call('cp '+filePath+' ./filterConfig/', shell=True)
        self.destroy()


    def applyFilterTypeButtonPressed(self,filePath,headCheckButtonInt,jawCheckButtonInt):

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



                