from filterTypesConfig.eguanaFilterTypesConfig import EguanaFilterTypesConfig
import numpy as np
from matplotlib.mlab import PCA

class ErFilter(EguanaFilterTypesConfig):

	def __init__(self):
	
		EguanaFilterTypesConfig.__init__(self)
		self.name = "ER Filter"
		self.filterType = "Jaw"
		
	def filter (articulatorSignalList,referenceSignalList):
		"""
		assume only X, Y, Z data is needed (no need for angle measurements)
		might need to adjust dimensions of articulatorSignalList and referenceSignalList depending on different
		machines or different filters
		"""
		
		ANGLE_PC_CORRELATION_CONST = 0.52;
		"""
		check the size of lists
		"""
		if (articulatorSignalList.shape[0] == referenceSignalList.shape[0] and articulatorSignalList.shape[1] == referenceSignalList.shape[1]):
			
			"""
			take out the Y component to calculate PCA
			"""
			ref_list_ignore_Y = scipy.delete(referenceSignalList,1,1);
			dataList = np.array (ref_list_ignore_Y);
			
			"""
			do PCA on dataList, then calculate alpha using the experimentally determined correlation constant
			"""
			
			alpha = ANGLE_PC_CORRELATION_CONST * (PCA (dataList))[0];
			
			""" transformation of articulatorSignalList to correctedList
			"""
			ss_ref_arti = referenceSignalList - articulatorSignalList;
			
			for i in range(len(alpha)): 
				correctedList[0][i] = cos(alpha[i]) * ss_ref_arti[0][i] + sin(alpha[i]) * ss_ref_arti[2][i];
				correctedList[1][i] = ss_ref_arti[1][i];
				correctedList[2][i] = -sin(alpha[i]) * ss_ref_arti[0][i] + cos(alpha[i]) * ss_ref_arti[2][i];
				
			return correctedList;
		else:
			return none;

