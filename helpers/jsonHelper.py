import json
from eguanaModel import EguanaModel



def getAllMachineFileNames():
    #gets all machine filenames
    with open('config.json') as data_file:    
        data = json.load(data_file)

    machineFilenameList = data['allMachines']
    
    return machineFilenameList

def getAllGroups():
    with open("./config.json", 'r') as f:
        configJSONDict = json.loads(f.read())

    return configJSONDict["allGroups"]    


def getAllModulesFileNames():
    with open("./config.json", 'r') as f:
        configJSONDict = json.loads(f.read())

    return configJSONDict["allModules"]   

def getAllHeadFiltersFileNames():
    with open("./config.json", 'r') as f:
        configJSONDict = json.loads(f.read())

    return configJSONDict["allHeadFilterTypes"]  

def getAllJawFiltersFileNames():
    with open("./config.json", 'r') as f:
        configJSONDict = json.loads(f.read())

    return configJSONDict["allJawFilterTypes"]  

def getHeadFiltersListForGroup(groupName):
    
    with open("./config.json", 'r') as f:
        configJSONDict = json.loads(f.read())

    groupConfigArray = configJSONDict['groupConfig']

    for groupDict in groupConfigArray:
        if groupDict['groupName'] == groupName:
            return groupDict["headFilters"]

    return []


def getJawFiltersListForGroup(groupName):
    with open("./config.json", 'r') as f:
        configJSONDict = json.loads(f.read())

    groupConfigArray = configJSONDict['groupConfig']

    for groupDict in groupConfigArray:
        if groupDict['groupName'] == groupName:
            return groupDict["jawFilters"]

    return []
    
def getModuleListForGroup(groupName):
    with open("./config.json", 'r') as f:
        configJSONDict = json.loads(f.read())

    groupConfigArray = configJSONDict['groupConfig']
    
    for groupDict in groupConfigArray:
        if groupDict['groupName'] == groupName:
            return groupDict["modules"]

    return []

def getAllGroupsForMachineFilename(machineFilename):
    
    with open("./config.json", 'r') as f:
        configJSONDict = json.loads(f.read())

    machineConfigArray = configJSONDict['machineConfig']
    
    for machineDict in machineConfigArray:
        if machineDict['machineName'] == machineFilename:
            return machineDict["groups"]

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





def removeMachineFromJSONForMachine(machineFileName):
        
    with open("./config.json", 'r') as f:
        configJSONDict = json.loads(f.read())


    machineConfigArray = configJSONDict["machineConfig"]


    for machineDict in machineConfigArray:
        if machineDict["machineName"] == machineFileName:
            machineConfigArray.remove(machineDict)
            break


    configJSONDict["allMachines"].remove(machineFileName)

    with open("./config.json", 'w') as f:
        json.dump(configJSONDict,f)


def removeFilterTypeFromJSONForFilterType(selectedFilterFileName,filterType):
        
    filterTypeJsonName = 'headFilters'
    allFilterTypeJsonName = 'allHeadFilterTypes'

    if filterType == 'Jaw':
        filterTypeJsonName = 'jawFilters'
        allFilterTypeJsonName = 'allJawFilterTypes'

    with open("./config.json", 'r') as f:
        configJSONDict = json.loads(f.read())

    groupConfigArray = configJSONDict["groupConfig"]

    for groupDict in groupConfigArray:
        filterTypeList = groupDict[filterTypeJsonName]
        if selectedFilterFileName in filterTypeList:
            filterTypeList.remove(selectedFilterFileName)

    if selectedFilterFileName in configJSONDict[allFilterTypeJsonName]:
        configJSONDict[allFilterTypeJsonName].remove(selectedFilterFileName)

    with open("./config.json", 'w') as f:
        json.dump(configJSONDict,f)


def addFilterTypeToJSON(fileName,groupNameList,filterType):

    with open("./config.json", 'r') as f:
        configJSONDict = json.loads(f.read())

    groupConfigArray = configJSONDict["groupConfig"]

    for groupConfigDict in groupConfigArray:
        if groupConfigDict["groupName"] in groupNameList:
            filterList = groupConfigDict["headFilters"]
            if filterType == 'Jaw':
                filterList = groupConfigDict["jawFilters"]

            if (fileName not in filterList):  
                filterList.append(fileName)

    allFilterList = configJSONDict["allHeadFilterTypes"]
    if filterType == 'Jaw':
        allFilterList = configJSONDict["allJawFilterTypes"]

    if (fileName not in allFilterList):  
        allFilterList.append(fileName)

    with open("./config.json", 'w') as f:
        json.dump(configJSONDict,f)


def removeModuleFromJSON(selectedModuleFileName):

    with open("./config.json", 'r') as f:
        configJSONDict = json.loads(f.read())

    groupConfigArray = configJSONDict["groupConfig"]

    for groupDict in groupConfigArray:
        moduleList = groupDict['modules']
        if selectedModuleFileName in moduleList:
            moduleList.remove(selectedModuleFileName)

    if selectedModuleFileName in configJSONDict['allModules']:
        configJSONDict['allModules'].remove(selectedModuleFileName)

    with open("./config.json", 'w') as f:
        json.dump(configJSONDict,f)    

def addModuleToJSON(fileName,groupNameList):

    with open("./config.json", 'r') as f:
        configJSONDict = json.loads(f.read())

    groupConfigArray = configJSONDict["groupConfig"]

    for groupConfigDict in groupConfigArray:
        if groupConfigDict["groupName"] in groupNameList:
            moduleList = groupConfigDict["modules"]
            if fileName not in moduleList:
                moduleList.append(fileName)

    allModuleList = configJSONDict["allModules"]
    
    if fileName not in allModuleList:
        allModuleList.append(fileName)

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


def addMachineToJSON(machineFileName,groupNamesList):


    with open("./config.json", 'r') as f:
        configJSONDict = json.loads(f.read())

    newMachineDict = {}
    newMachineDict["machineName"] = machineFileName
    newMachineDict["groups"] = groupNamesList

    machineConfigArray = configJSONDict["machineConfig"]

    machineConfigArray.append(newMachineDict)

    allMachinesList = configJSONDict["allMachines"]
    allMachinesList.append(machineFileName)

    with open("./config.json", 'w') as f:
        json.dump(configJSONDict,f)

