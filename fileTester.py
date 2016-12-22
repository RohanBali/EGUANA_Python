# import base class
from machineConfig.eguanaMachineConfig import EguanaMachineConfig
from filterTypesConfig.eguanaFilterTypesConfig import EguanaFilterTypesConfig
from moduleConfig.eguanaModuleConfig import EguanaModuleConfig

import importlib.util
import os.path
#import traceback

def __getErrorMessageForException(exception):
	errorMessage=exception.__class__.__name__ + ': '+exception.msg

	if isinstance(exception,SyntaxError):
		errorMessage+='\n'+exception.filename+', Line '+str(exception.lineno)
	#else:
		#errorMessage+='\nTraceback:\n'
		#tb=traceback.extract_tb(exception.__traceback__,3)
		#tblist=traceback.format_list(tb)
		#for tbRecord in tblist:
		#	errorMessage+=tbRecord
	
	return errorMessage

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
		errorMessage='exception raised when loading file:\n'+__getErrorMessageForException(e)
		return (False,None,errorMessage)

	if hasattr(testModule,className):
		classType=getattr(testModule,className)
		return (True,classType,'')
	else:
		return (False,None,'Class ' + className + ' do not exist')

def __testClassType(testClassType,baseClassType,testVector):
	'''testVector:[(functionName1,argumentList1,returnType1),(...)]'''
	if not issubclass(testClassType,baseClassType):
		errorMessage=testClassType.__name__ + ' is not derived from ' + baseClassType.__name__ + '.'
		return [False,errorMessage]
	
	#not sure if there is a way to check if the function is overwritten or not without instantiating the base class
	#if there is then this can be further improved
	try:
		baseClassInstance=baseClassType()
	except Exception as e:
		return [False,'Base class instantiation raises exception:\n'+__getErrorMessageForException(e)]
	
	try:
		testClassInstance=testClassType()
	except Exception as e:
		return [False, testClassType.__name__ + ' instantiation raises exception:\n'+__getErrorMessageForException(e)]
	
	errorMessageList=[]
	for testVectorIndex in range(0,len(testVector)):
		currentFunctionName=testVector[testVectorIndex][0]
		currentFunctionArgument=testVector[testVectorIndex][1]
		currentFunctionExpectedReturnType=testVector[testVectorIndex][2]
		
		baseFunction = getattr(baseClassInstance,currentFunctionName)
		currFunction = getattr(testClassInstance,currentFunctionName)
		
		if baseFunction.__func__ is currFunction.__func__:
			errorMessageList.append(currentFunctionName + ' is not overwritten')
		else:
			try:
				currentTestReturnValue=getattr(testClassInstance,currentFunctionName)(*currentFunctionArgument)
				if type(currentTestReturnValue) is not currentFunctionExpectedReturnType:
					errorMessageList.append(currentFunctionName + ' do not return expected type')
			
			except Exception as e:
				errorMessageList.append(currentFunctionName + ' raises exception in testing:\n' + __getErrorMessageForException(e))
	
	if errorMessageList:
		errorMessage = 'Problem in ' + testClassType.__name__ + ':'
		for currentMessage in errorMessageList:
			errorMessage += '\n' + currentMessage

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

__ModuleConfig_TestVector=[]

def testMachineConfig(testClassFilePath):
	return __testFile(testClassFilePath,EguanaMachineConfig,__MachineConfig_TestVector)

def testHeadFilter(testClassFilePath):
	return __testFile(testClassFilePath,EguanaFilterTypesConfig,__HeadFilter_TestVector)

def testJawFilter(testClassFilePath):
	return __testFile(testClassFilePath,EguanaFilterTypesConfig,__JawFilter_TestVector)

def testModuleConfig(testClassFilePath):
	return __testFile(testClassFilePath,EguanaModuleConfig,__ModuleConfig_TestVector)
