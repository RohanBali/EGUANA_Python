from filterTypesConfig.eguanaFilterTypesConfig import EguanaFilterTypesConfig

class JsonFilterTypeConfig(EguanaFilterTypesConfig):
	def __init__(self):
		EguanaFilterTypesConfig.__init__(self)  
		self.name = "JSON Filter" 
		self.filterType = "Jaw"

