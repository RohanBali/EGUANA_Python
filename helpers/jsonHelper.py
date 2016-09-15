import json


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
	