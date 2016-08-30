from filterTypesConfig.eguanaFilterTypesConfig import EguanaFilterTypesConfig

class RHenriquesFilter(EguanaFilterTypesConfig):
	def __init__(self):
		EguanaFilterTypesConfig.__init__(self)   
		self.name = "R Henriques"
		self.filterType = "Head"

