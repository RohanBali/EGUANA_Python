from filterTypesConfig.eguanaFilterTypesConfig import EguanaFilterTypesConfig

class SsFilter(EguanaFilterTypesConfig):
	name = "Simple Substraction"
	filterType = "Jaw"
	
	def __init__(self):
		EguanaFilterTypesConfig.__init__(self)   

