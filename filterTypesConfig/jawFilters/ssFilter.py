from filterTypesConfig.eguanaFilterTypesConfig import EguanaFilterTypesConfig

class SsFilter(EguanaFilterTypesConfig):
	def __init__(self):
		EguanaFilterTypesConfig.__init__(self)   
		self.name = "Simple Substraction"
		self.filterType = "Jaw"