from filterTypesConfig.eguanaFilterTypesConfig import EguanaFilterTypesConfig

class GoldFilter(EguanaFilterTypesConfig):
	name = "Gold" 
	filterType = "Jaw"

	def __init__(self):
		EguanaFilterTypesConfig.__init__(self)  

