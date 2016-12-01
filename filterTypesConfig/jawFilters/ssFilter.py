from filterTypesConfig.eguanaFilterTypesConfig import EguanaFilterTypesConfig
import numpy


class SsFilter(EguanaFilterTypesConfig):

	def __init__(self):
	
		EguanaFilterTypesConfig.__init__(self)   
		self.name = "Simple Substraction"
		self.filterType = "Jaw"
	
	def filter(articulatorSignalList,referenceSignalList):	
	
		if (articulatorSignalList.shape[0] == referenceSignalList.shape[0] && articulatorSignalList.shape[1] == referenceSignalList.shape[1])
			return referenceSignalList - articulatorSignalList;
		else
			return none;
		