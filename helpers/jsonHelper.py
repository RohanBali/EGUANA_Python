import json
from eguanaModel import EguanaModel


def getEnabledFilterFunctionsNameForMachineFilename(machineFilename):

	with open("./config.json", 'r') as f:
		configJSONDict = json.loads(f.read())

	configArray = configJSONDict["configurations"]

	tmpDict = None

	for configDict in configArray:
		if configDict['machineName'] == machineFilename:
			tmpDict = configDict
			break

	if tmpDict:

		filterFunctionsList = tmpDict['filterFunctions']

		enabledFilterFunctionNameList = []

		for filterFunctionDict in filterFunctionsList:
			enabledFilterFunctionNameList.append(filterFunctionDict['filterApplicationName'])

		return enabledFilterFunctionNameList

   
	return []


def getEnabledJawFilterFunctionFileNamesForMachineAndFilterFunctionFileNames(machineFilename,filterFunctionFilename):


	with open("./config.json", 'r') as f:
		configJSONDict = json.loads(f.read())

	configArray = configJSONDict["configurations"]

	tmpDict = None

	for configDict in configArray:
		if configDict['machineName'] == machineFilename:
			tmpDict = configDict
			break

	if tmpDict:

		filterFunctionsList = tmpDict['filterFunctions']

		enabledFilterFunctionNameList = []

		for filterFunctionDict in filterFunctionsList:

			if filterFunctionDict['filterApplicationName'] == filterFunctionFilename:
				return filterFunctionDict['filterTypes']['jawFilter']
			

   
	return []



def getEnabledHeadFilterFunctionFileNamesForMachineAndFilterFunctionFileNames(machineFilename,filterFunctionFilename):


	with open("./config.json", 'r') as f:
		configJSONDict = json.loads(f.read())

	configArray = configJSONDict["configurations"]

	tmpDict = None

	for configDict in configArray:
		if configDict['machineName'] == machineFilename:
			tmpDict = configDict
			break

	if tmpDict:

		filterFunctionsList = tmpDict['filterFunctions']

		enabledFilterFunctionNameList = []

		for filterFunctionDict in filterFunctionsList:

			if filterFunctionDict['filterApplicationName'] == filterFunctionFilename:
				return filterFunctionDict['filterTypes']['headFilters']
   
	return []


def getEnabledMachineNameForFilterFunctionFilename(filterFunctionFilename):

	with open("./config.json", 'r') as f:
		configJSONDict = json.loads(f.read())

	configArray = configJSONDict["configurations"]

	enabledMachineFilenameList = []

	for machineConfigDict in configArray:

		for filterFunctionsDict in machineConfigDict['filterFunctions']:
			if filterFunctionsDict['filterApplicationName'] == filterFunctionFilename:
				enabledMachineFilenameList.append(machineConfigDict['machineName'])
				break

	return enabledMachineFilenameList
	

def getEnabledMachineNameForFilterTypeFilename(filterTypeFilename,filterType):

	with open("./config.json", 'r') as f:
		configJSONDict = json.loads(f.read())

	configArray = configJSONDict["configurations"]

	if filterType == 'Head':
		filterTypeName = filterType.lower() + 'Filters'
	elif filterType == 'Jaw':
		filterTypeName = filterType.lower() + 'Filter'

	enabledMachineFilenameList = []

	for machineConfigDict in configArray:

		for filterFunctionsDict in machineConfigDict['filterFunctions']:
			filterTypeNameArray = filterFunctionsDict['filterTypes'][filterTypeName]
			if filterTypeFilename in filterTypeNameArray:
				enabledMachineFilenameList.append(machineConfigDict['machineName'])
				break			

	return enabledMachineFilenameList



def getEnabledFilterFunctionFileNamesForMachineAndFilterTypeFileNames(machineFilename,filterTypeFilename,filterType):

	with open("./config.json", 'r') as f:
		configJSONDict = json.loads(f.read())

	configArray = configJSONDict["configurations"]

	if filterType == 'Head':
		filterTypeName = filterType.lower() + 'Filters'
	elif filterType == 'Jaw':
		filterTypeName = filterType.lower() + 'Filter'

	enabledFilterFunctionNameList = []

	for machineConfigDict in configArray:

		if machineConfigDict['machineName'] == machineFilename:

			for filterFunctionsDict in machineConfigDict['filterFunctions']:
				filterTypeNameArray = filterFunctionsDict['filterTypes'][filterTypeName]
				if filterTypeFilename in filterTypeNameArray:
					enabledFilterFunctionNameList.append(filterFunctionsDict['filterApplicationName'])

	return enabledFilterFunctionNameList


def removeMachineFromJSONForMachine(machine):
        
    with open("./config.json", 'r') as f:
        configJSONDict = json.loads(f.read())

    configArray = configJSONDict["configurations"]

    for machineDict in configArray:
        if machineDict["machineName"] == machine.getFilename():
            configArray.remove(machineDict)
            break


    configJSONDict["allMachines"].remove(machine.getFilename())

    with open("./config.json", 'w') as f:
        json.dump(configJSONDict,f)

def removeFilterFunctionFromJSONForFilterFunction(filterFunctionObject):
        
    with open("./config.json", 'r') as f:
        configJSONDict = json.loads(f.read())

    configArray = configJSONDict["configurations"]

    for machineDict in configArray:
    	filterFunctionsArray = machineDict['filterFunctions']
    	for filterFunctionDict in filterFunctionsArray:
    		if filterFunctionDict['filterApplicationName'] == filterFunctionObject.getFilename():
    			filterFunctionsArray.remove(filterFunctionDict)
    			break


    configJSONDict["allFilterFunctions"].remove(filterFunctionObject.getFilename())

    with open("./config.json", 'w') as f:
        json.dump(configJSONDict,f)


def removeFilterTypeFromJSONForFilterType(selectedFilterTypeObject,filterType):
        
    filterTypeJsonName = 'headFilters'
    allFilterTypeJsonName = 'allHeadFilterTypes'

    if filterType == 'Jaw':
        filterTypeJsonName = 'jawFilter'
        allFilterTypeJsonName = 'allJawFilterTypes'

    with open("./config.json", 'r') as f:
        configJSONDict = json.loads(f.read())

    configArray = configJSONDict["configurations"]

    for machineDict in configArray:
    	filterFunctionsArray = machineDict['filterFunctions']
    	for filterFunctionDict in filterFunctionsArray:
    		filterTypeArray = filterFunctionDict['filterTypes'][filterTypeJsonName]
    		filterTypeArray.remove(selectedFilterTypeObject.getFilename())


    configJSONDict[allFilterTypeJsonName].remove(selectedFilterTypeObject.getFilename())

    with open("./config.json", 'w') as f:
        json.dump(configJSONDict,f)


def addFilterTypeToJSON(filterFunctionObject,filterTypeFrameList,filterType):
     
    filterTypeJsonName = 'headFilters'
    allFilterTypeJsonName = 'allHeadFilterTypes'

    if filterType == 'Jaw':
        filterTypeJsonName = 'jawFilter'
        allFilterTypeJsonName = 'allJawFilterTypes'


    with open("./config.json", 'r') as f:
        configJSONDict = json.loads(f.read())

    configArray = configJSONDict["configurations"]

    allMachineFilenameList = EguanaModel().getAllMachines()
    
    atleastOneMachineEnabled = False


    for machineDict in configArray:

        if filterTypeFrameList[allMachineFilenameList.index(machineDict['machineName'])].isEnabled():

            enabledFfFilenameList = filterTypeFrameList[allMachineFilenameList.index(machineDict['machineName'])].getEnabledFilterFunctionNames()

            for ffFileName in enabledFfFilenameList:

                atleastOneMachineEnabled = True

                ffDict = None

                for ffDictTmp in machineDict['filterFunctions']:
                    if ffFileName in ffDictTmp['filterApplicationName']:
                        ffDict = ffDictTmp
                        break

                if ffDict == None:
                    newFilterFunctionDict = {}
                    newFilterFunctionDict['filterApplicationName'] = ffFileName
                    filterTypesDict = {}
                    filterTypesDict['headFilters'] = []
                    filterTypesDict['jawFilters'] = []
                    filterTypesDict[filterTypeJsonName].append(filterFunctionObject.getFilename())
                    newFilterFunctionDict['filterTypes'] = filterTypesDict
                    filterFunctionsArray = machineDict['filterFunctions']
                    filterFunctionsArray.append(newFilterFunctionDict)
                else:
                    ffDict['filterTypes'][filterTypeJsonName].append(filterFunctionObject.getFilename())


    if atleastOneMachineEnabled:
        configJSONDict[allFilterTypeJsonName].append(filterFunctionObject.getFilename())


    with open("./config.json", 'w') as f:
        json.dump(configJSONDict,f)



def addFilterFunctionToJSON(filterFunctionObject,filterTypeFrameList):
        
    with open("./config.json", 'r') as f:
        configJSONDict = json.loads(f.read())

    configArray = configJSONDict["configurations"]

    allMachineFilenameList = EguanaModel().getAllMachines()
    
    for machineDict in configArray:
        if filterTypeFrameList[allMachineFilenameList.index(machineDict['machineName'])].isEnabled():

            newFilterFunctionDict = {}
            newFilterFunctionDict['filterApplicationName'] = filterFunctionObject.getFilename()

            filterTypesDict = {}
            filterTypesDict['headFilters'] = filterTypeFrameList[allMachineFilenameList.index(machineDict['machineName'])].getEnabledHeadFilterTypeNames()
            filterTypesDict['jawFilters'] = filterTypeFrameList[allMachineFilenameList.index(machineDict['machineName'])].getEnabledJawFilterTypeNames()

            newFilterFunctionDict['filterTypes'] = filterTypesDict

            filterFunctionsArray = machineDict['filterFunctions']
            filterFunctionsArray.append(newFilterFunctionDict)


    allFilterFuctions = configJSONDict["allFilterFunctions"]
    allFilterFuctions.append(filterFunctionObject.getFilename())


    with open("./config.json", 'w') as f:
        json.dump(configJSONDict,f)


def addMachineToJSON(selectedMachine,filterTypeFrameList):


    with open("./config.json", 'r') as f:
        configJSONDict = json.loads(f.read())

    configArray = configJSONDict["configurations"]
    allFilterFunctionFunctionNameList = EguanaModel().getAllFilterFunctions()

    newMachineDict = {}

    newMachineDict["machineName"] = selectedMachine.getFilename()

    newFilterFunctionsList = []

    for i in range(len(filterTypeFrameList)):
        if filterTypeFrameList[i].isEnabled():
            newFilterFunctionDict = {}
            newFilterFunctionDict["filterApplicationName"] =  EguanaModel().getFilterObjectFromFunctionName(allFilterFunctionFunctionNameList[i]).getFilename()

            filterTypesDict = {}

            filterTypesDict['headFilters'] = filterTypeFrameList[i].getEnabledHeadFilterTypeNames()
            filterTypesDict['jawFilters'] = filterTypeFrameList[i].getEnabledJawFilterTypeNames()

            newFilterFunctionDict['filterTypes'] = filterTypesDict
            newFilterFunctionsList.append(newFilterFunctionDict)

    newMachineDict['filterFunctions'] = newFilterFunctionsList
    configArray.append(newMachineDict)

    allMachinesList = configJSONDict["allMachines"]
    allMachinesList.append(selectedMachine.getFilename())


    with open("./config.json", 'w') as f:
    	json.dump(configJSONDict,f)



