from filterTypesConfig.eguanaFilterTypesConfig import EguanaFilterTypesConfig

class PosFilter(EguanaFilterTypesConfig):
	def __init__(self):
		EguanaFilterTypesConfig.__init__(self)
		self.name = "Pos Folder"
		self.filterType = "Head"

