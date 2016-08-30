import sys

class EguanaFilterTypesConfig():
	def __init__(self):
		self.name = ""

		self.filterType = None

	def getFilename(self):
		fullPath =  sys.modules[self.__class__.__module__].__file__
		components = fullPath.split('/')
		return components[-1]