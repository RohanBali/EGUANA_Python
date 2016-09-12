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









