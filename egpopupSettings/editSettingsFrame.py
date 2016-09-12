from tkinter import *
from eguanaModel import EguanaModel

class EditSettingsFrame(Frame):
    def __init__(self,notebook):
        Frame.__init__(self,notebook)
        self.currentValue = None

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

        if value != self.currentValue:

            self.currentValue = value

            for i in range(3,self.grid_size()[1]): 
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
                a = 1
            else: #'Filter Type'
                b = 1


    def machineSelectedFromOptionsMenu(self,value):
    	machineNamesList = EguanaModel().getAllMachines()

    	selectedMachine = None

    	for machineFileName in machineNamesList:
    		if EguanaModel().getMachineObjectFromMachineName(machineFileName).name == value:
    			selectedMachine = EguanaModel().getMachineObjectFromMachineName(machineFileName)
    			break


    	if selectedMachine:
    		self.setupSelectedMachineConfig(selectedMachine)




    def setupSelectedMachineConfig(self,selectedMachine):

    	# create a notebook
    	#get a list of all filter function names, and head and jaw filters
    	# loop through them
    	# for each check if it is already selected or not
    	# if it is selected, check if the corresponding head and jaw fitlers are also selected
    	# pass this info to filtertypecheckbox frame subclassed

    	filterFunctionNotebook = Notebook(self)
    	filterFunctionNotebook.grid(row=3, column=0,columnspan=4, sticky=E+W)

    	allFilterFunctionFilenames = EguanaModel().getAllFilterFunctions()
        allHeadList = EguanaModel().getAllHeadFilterTypes()
        allJawList = EguanaModel().getAllJawFilterTypes()

    	allFilterFunctionObjects = [EguanaModel().getFilterObjectFromFunctionName(fileName) for fileName in allFilterFunctionFilenames]
    	allHeadFiltersTypeObjects = EguanaModel().getFilterTypeObjectsFromTypeNameArray(allHeadList,'Head')
    	allJawFilterTypeObjects = EguanaModel().getFilterTypeObjectsFromTypeNameArray(allJawList,'Jaw')


    	for filterFunction in allFilterFunctionObjects:
    		filterFunctionEnabledBool = self.isFilterFunctionEnabledForMachine(filterFunction,selectedMachine)
    		headFilterEnabledBoolList = [self.isHeadFilterEnabledForMachine(headFilter,selectedMachine) for headFilter in allHeadFiltersTypeObjects]
    		jawFilterEnabledBoolList = [self.isJawFilterEnabledForMachine(jawFilter,selectedMachine) for jawFilter in allJawFilterTypeObjects]

    		filterFunctionFrame = FilterTypeCheckboxFrame(filterFunctionNotebook,allHeadFiltersTypeObjects,allJawFilterTypeObjects,filterFunctionEnabledBool,headFilterEnabledBoolList,jawFilterEnabledBoolList)
    		filterFunctionFrame.pack(fill=BOTH, expand=True)
    		filterFunctionNotebook.add(filterFunctionFrame, text=filterFunction.name)


# dropList = EguanaModel().getAllFilterFunctions()

# headList = EguanaModel().getAllHeadFilterTypes()
# modifiedHeadList = EguanaModel().getFilterTypeObjectsFromTypeNameArray(headList,'Head')

# jawList = EguanaModel().getAllJawFilterTypes()
# modifiedJawList = EguanaModel().getFilterTypeObjectsFromTypeNameArray(jawList,'Jaw')


# filterFunctionFrameList = []

# for i in range(len(dropList)):

# filterFunctionFrame = FilterTypeCheckboxFrame(filterFunctionNotebook,modifiedHeadList,modifiedJawList)
# filterFunctionFrameList.append(filterFunctionFrame)
# filterFunctionFrame.pack(fill=BOTH, expand=True)
# filterFunctionNotebook.add(filterFunctionFrame, text=EguanaModel().getFilterObjectFromFunctionName(dropList[i]).name)

