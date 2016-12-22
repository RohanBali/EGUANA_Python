from filterTypesConfig.eguanaFilterTypesConfig import EguanaFilterTypesConfig

class PosFilter(EguanaFilterTypesConfig):
	name = "Pos Folder"
	filterType = "Head"
	
	def __init__(self):
		EguanaFilterTypesConfig.__init__(self)

