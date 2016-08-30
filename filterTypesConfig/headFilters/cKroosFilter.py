from filterTypesConfig.eguanaFilterTypesConfig import EguanaFilterTypesConfig

class CKroosFilter(EguanaFilterTypesConfig):
	def __init__(self):
		EguanaFilterTypesConfig.__init__(self)  
		self.name = "C Kroos" 
		self.filterType = "Head"

