from filterTypesConfig.eguanaFilterTypesConfig import EguanaFilterTypesConfig
import numpy as np
from matplotlib.mlab import PCA
import math

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
		
		ANGLE_PC_CORRELATION_CONST = 0.52/180*math.pi;
		"""
		check the size of lists
		"""
		if (articulatorSignalList.shape[0] == referenceSignalList.shape[0] and articulatorSignalList.shape[1] == referenceSignalList.shape[1]):
			
			"""
			take out the Y component to calculate PCA
			"""
			ref_list_ignore_Y = np.delete(referenceSignalList,1,1);
			dataList = np.array (ref_list_ignore_Y);
			
			"""
			do PCA on dataList, then calculate alpha using the experimentally determined correlation constant
			"""
			
			alpha = ANGLE_PC_CORRELATION_CONST * (PCA (dataList)).Y[:,0];
			
			""" transformation of articulatorSignalList to correctedList
			"""
			ss_ref_arti = articulatorSignalList - referenceSignalList;
			correctedList = np.zeros((len(alpha),3))
			for i in range(len(alpha)): 
				correctedList[i][0] = np.cos(alpha[i]) * ss_ref_arti[i][0] + np.sin(alpha[i]) * ss_ref_arti[i][2];
				correctedList[i][1] = ss_ref_arti[i][1];
				correctedList[i][2] = -np.sin(alpha[i]) * ss_ref_arti[i][0] + np.cos(alpha[i]) * ss_ref_arti[i][2];
				
			return correctedList;
		else:
			return none;

