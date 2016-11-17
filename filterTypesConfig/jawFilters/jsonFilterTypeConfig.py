from filterTypesConfig.eguanaFilterTypesConfig import EguanaFilterTypesConfig

class JsonFilterTypeConfig(EguanaFilterTypesConfig):
	name = "JSON Filter" 
	filterType = "Jaw"
	def __init__(self):
		EguanaFilterTypesConfig.__init__(self)  

