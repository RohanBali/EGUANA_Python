from filterTypesConfig.eguanaFilterTypesConfig import EguanaFilterTypesConfig

class GoldFilter(EguanaFilterTypesConfig):
	def __init__(self):
		EguanaFilterTypesConfig.__init__(self)  
		self.name = "Gold" 
		self.filterType = "Jaw"

