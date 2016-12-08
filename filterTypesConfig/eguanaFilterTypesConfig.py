import sys

class EguanaFilterTypesConfig():
	def __init__(self):
		self.name = ""

		self.filterType = None

	def getFilename(self):
		fullPath =  sys.modules[self.__class__.__module__].__file__
		components = fullPath.split('/')
		return components[-1]

	def filter(articulatorSignalList,referenceSignalList):
	    """
	    	articlulatorSignalList --- Rows represent values across time
	    						   --- Columns represent values across dimensions

	    	referenceSignalList --- Rows represent values across time
	    				  --- Columns represent values across dimensions

			Both articulatorSignalList and referenceSignalList should have same size

	    """
	    return 0;