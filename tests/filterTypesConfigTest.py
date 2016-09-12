from filterTypesConfig.eguanaFilterTypesConfig import EguanaFilterTypesConfig
import importlib.util


class FilterTypesConfigTest():
	
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

		if isinstance(self.testClass,EguanaFilterTypesConfig):
			return [True,errorString]
		else:
			return [False,"Not inherited from base class"]


	def checkIfMethodsAreOverwritte(self):

		# todo

		return [True,'']









