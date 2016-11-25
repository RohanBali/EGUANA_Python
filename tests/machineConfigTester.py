from machineConfig.eguanaMachineConfig import EguanaMachineConfig
import importlib.util

import os.path
def testMachineConfig(testClassFilePath):
	'''This function tests if the given file is a valid machine config file'''
	
	def fileRelatedCheck(filePath):
		'''return value: (isCheckSuccess,classVal,errorMessage)'''
		if not os.path.isfile(filePath):
			return (False,None,'File do not exist')
		
		fileName=os.path.basename(filePath)
		fileNameTemp,extension=os.path.splitext(fileName)
		className=fileNameTemp[0].upper()+fileNameTemp[1:]
		#currently no check on extension
		try:
			spec = importlib.util.spec_from_file_location(fileName, filePath)
			testModule = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(testModule)
		except Exception as e:
			return (False,None,'exception raised when loading config file ('+str(e)+')')

		if hasattr(testModule,className):
			classType=getattr(testModule,className)
			return (True,classType,'')
		else:
			return (False,None,'Class ' + className + ' do not exist')

	def classRelatedCheck(testClass):
		errorMessageList=[]
		functionNameTuple=('isDirectoryValid','ifTrialExists','getDataForTrialNumber')
		functionArgumentTuple=('',0,0)
		functionExpectedReturnValueTuple=(type(False),type(False),type([]))
		baseClass = EguanaMachineConfig()

		for functionIndex in range(0,3):
			currentFunctionName=functionNameTuple[functionIndex]
			currentFunctionArgument=functionArgumentTuple[functionIndex]
			currentFunctionExpectedReturnType=functionExpectedReturnValueTuple[functionIndex]
			baseFunction = getattr(baseClass,currentFunctionName)
			currFunction = getattr(testClass,currentFunctionName)
			if baseFunction.__func__ is not currFunction.__func__:
				try:
					currentTestReturnValue=getattr(testClass,currentFunctionName)(currentFunctionArgument)
					if type(currentTestReturnValue) is not currentFunctionExpectedReturnType:
						currentErrorMessage = currentFunctionName + ' do not return expected type'
						errorMessageList.append(currentErrorMessage)

				except Exception as e:
					currentErrorMessage = currentFunctionName + ' raises exception in testing (' + str(e) + ')'
					errorMessageList.append(currentErrorMessage)

			else:
				currentErrorMessage = currentFunctionName + ' is not overwritten'
				errorMessageList.append(currentErrorMessage)
		
		#empty list is false
		if errorMessageList:
			errorMessage = str(len(errorMessageList)) + ' error(s) in total:'
			for currentMessage in errorMessageList:
				errorMessage += ' ' + currentMessage

			return [False,errorMessage]
		else:
			return [True,'']
	
	isFirstTestGood,classType,errorMessage=fileRelatedCheck(testClassFilePath)
	if isFirstTestGood:
		if issubclass(classType,EguanaMachineConfig):
			try:
				testClassInstance=classType()
			except Exception as e:
				return [False,'Error: test class instantiation raises exception ('+str(e)+')']
			else:
				return classRelatedCheck(testClassInstance)
		else:
			return [False,'Error: test class is not derived from EguanaMachineConfig']
	else:
		return [False,errorMessage]

