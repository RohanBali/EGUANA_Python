from machineConfig.eguanaMachineConfig import EguanaMachineConfig
import importlib.util


class MachineConfigTest():
	
	def __init__(self,testClassFilePath):

		components = testClassFilePath.split('/')
		fileName = components[-1]

		moduleNameComponents = fileName.split('.')
		moduleName = moduleNameComponents[0]

		spec = importlib.util.spec_from_file_location(fileName, testClassFilePath)
		testModule = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(testModule)


		if hasattr(testModule, moduleName[0].upper() + moduleName[1:]):
			classVar = getattr(testModule,moduleName[0].upper() + moduleName[1:])
			self.testClass = classVar()
		else:
			self.testClass = None

	oldCode='''
	def runTests(self):

		errorString = ""

		[returnValue,errorString] = self.existsTest()
		
		if returnValue == False:
			return [returnValue,errorString]


		[returnValue,errorString] = self.runClassTest()

		if returnValue == False:
			return [returnValue,errorString]

		[returnValue,errorString] = self.checkIfMethodsAreOverwritte()

		if returnValue == False:
			return [returnValue,errorString]

		return [True,""]


	def existsTest(self):

		if self.testClass:
			return [True,'']
		else:
			return [False,'The class does not exist in file']

	def runClassTest(self):
		errorString = ""

		if isinstance(self.testClass,EguanaMachineConfig):
			return [True,errorString]
		else:
			return [False,"Not inherited from base class"]


	def checkIfMethodsAreOverwritte(self):

		functionNames = ['isDirectoryValid','ifTrialExists','setDirPath','getDataForTrialNumber']

		baseClass = EguanaMachineConfig()

		baseFunction = getattr(baseClass,'isDirectoryValid')
		currFunction = getattr(self.testClass,'isDirectoryValid')

		if baseFunction.__func__ is currFunction.__func__:
			return [False,'Please overwrite isDirectoryValid']


		baseFunction = getattr(baseClass,'ifTrialExists')
		currFunction = getattr(self.testClass,'ifTrialExists')

		if baseFunction.__func__ is currFunction.__func__:
			return [False,'Please overwrite ifTrialExists']




		baseFunction = getattr(baseClass,'setDirPath')
		currFunction = getattr(self.testClass,'setDirPath')

		if baseFunction.__func__ is currFunction.__func__:
			return [False,'Please overwrite setDirPath']




		baseFunction = getattr(baseClass,'isDirectoryValid')
		currFunction = getattr(self.testClass,'isDirectoryValid')

		if baseFunction.__func__ is currFunction.__func__:
			return [False,'Please overwrite isDirectoryValid']



		baseFunction = getattr(baseClass,'getDataForTrialNumber')
		currFunction = getattr(self.testClass,'getDataForTrialNumber')

		if baseFunction.__func__ is currFunction.__func__:
			return [False,'Please overwrite getDataForTrialNumber']


		return [True,'']
'''

	def runTests(self):

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
			currFunction = getattr(self.testClass,currentFunctionName)
			if baseFunction.__func__ is not currFunction.__func__:
				try:
					currentTestReturnValue=getattr(self.testClass,currentFunctionName)(currentFunctionArgument)
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



