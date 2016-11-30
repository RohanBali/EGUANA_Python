# import base class
from machineConfig.eguanaMachineConfig import EguanaMachineConfig
from filterTypesConfig.eguanaFilterTypesConfig import EguanaFilterTypesConfig

import importlib.util
import os.path

def __extractModuleFromFile(filePath):
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

def __testClassType(testClassType,baseClassType,testVector):
	'''testVector:[(functionName1,argumentList1,returnType1),(...)]'''
	if not issubclass(testClassType,baseClassType):
		errorMessage='Error: ' + testClassType.__name__ + ' is not derived from ' + baseClassType.__name__ + '.'
		return [False,errorMessage]
	
	#not sure if there is a way to check if the function is overwritten or not without instantiating the base class
	#if there is then this can be further improved
	try:
		baseClassInstance=baseClassType()
	except Exception as e:
		return [False,'Error: base class instantiation raises exception ('+str(e)+')']
	
	try:
		testClassInstance=testClassType()
	except Exception as e:
		return [False,'Error: test class instantiation raises exception ('+str(e)+')']
	
	errorMessageList=[]
	for testVectorIndex in range(0,len(testVector)):
		currentFunctionName=testVector[testVectorIndex][0]
		currentFunctionArgument=testVector[testVectorIndex][1]
		currentFunctionExpectedReturnType=testVector[testVectorIndex][2]
		
		baseFunction = getattr(baseClassInstance,currentFunctionName)
		currFunction = getattr(testClassInstance,currentFunctionName)
		
		errorMessageBeginning='In test ' + str(testVectorIndex+1)+ ': ' + currentFunctionName
		
		if baseFunction.__func__ is currFunction.__func__:
			errorMessageList.append(errorMessageBeginning + ' is not overwritten')
		else:
			try:
				currentTestReturnValue=getattr(testClassInstance,currentFunctionName)(*currentFunctionArgument)
				if type(currentTestReturnValue) is not currentFunctionExpectedReturnType:
					errorMessageList.append(errorMessageBeginning + ' do not return expected type')
			
			except Exception as e:
				errorMessageList.append(errorMessageBeginning + ' raises exception in testing (' + str(e) + ')')
	
	if errorMessageList:
		errorMessage = str(len(errorMessageList)) + ' error(s) in total:'
		for currentMessage in errorMessageList:
			errorMessage += ' ' + currentMessage

		return [False,errorMessage]
	else:
		return [True,'']

def __testFile(filePath,baseClassType,testVector):
	isCheckSuccess,classType,errorMessage=__extractModuleFromFile(filePath)
	if isCheckSuccess:
		return __testClassType(classType,baseClassType,testVector)
	else:
		return [False,errorMessage]

####################################################################################################

__MachineConfig_TestVector=[('isDirectoryValid',[''],type(False)),
			('ifTrialExists',[0],type(False)),
			('getDataForTrialNumber',[0],type([]))]

__HeadFilter_TestVector=[]

__JawFilter_TestVector=[]

def testMachineConfig(testClassFilePath):
	return __testFile(testClassFilePath,EguanaMachineConfig,__MachineConfig_TestVector)

def testHeadFilter(testClassFilePath):
	return __testFile(testClassFilePath,EguanaFilterTypesConfig,__HeadFilter_TestVector)

def testJawFilter(testClassFilePath):
	return __testFile(testClassFilePath,EguanaFilterTypesConfig,__JawFilter_TestVector)
