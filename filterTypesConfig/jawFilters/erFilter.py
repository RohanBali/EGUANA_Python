from filterTypesConfig.eguanaFilterTypesConfig import EguanaFilterTypesConfig

class ErFilter(EguanaFilterTypesConfig):
	def __init__(self):
		EguanaFilterTypesConfig.__init__(self)
		self.name = "ER Filter"
		self.filterType = "Jaw"

