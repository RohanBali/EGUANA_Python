from filterTypesConfig.eguanaFilterTypesConfig import EguanaFilterTypesConfig

class CKroosFilter(EguanaFilterTypesConfig):
	name = "C Kroos" 
	filterType = "Head"
	
	def __init__(self):
		EguanaFilterTypesConfig.__init__(self)  

