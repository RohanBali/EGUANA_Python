import sys

class EguanaModuleConfig():

	name = ""

	def __init__(self):
		return

	def getFilename(self):
		fullPath =  sys.modules[self.__class__.__module__].__file__
		components = fullPath.split('/')
		return components[-1]