from filterTypesConfig.eguanaFilterTypesConfig import EguanaFilterTypesConfig
import numpy as np
#from matplotlib.mlab import PCA
from sklearn.decomposition import PCA
from filterTypesConfig.jawFilters.joanaFilter import JoanaFilter
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
			# LH = referenceSignalList[:,[3,4,5]]
			# '''print (LH_Vector[1])'''
			# RH = referenceSignalList[:,[6,7,8]]
			# FH = referenceSignalList[:,[9,10,11]]
			# jaw = referenceSignalList[:,[0,1,2]]
			
			# hc_Jaw = JoanaFilter.filter(jaw, )
			
			
			dataList = np.column_stack((referenceSignalList[:,0],referenceSignalList[:,2]))	
			ref_list_ignore_Y = np.delete(referenceSignalList,1,1);
			dataList = np.array (dataList);
			#print (dataList)
			
			"""
			do PCA on dataList, then calculate alpha using the experimentally determined correlation constant
			"""
			p = PCA (n_components=2)
			myPCA = p.fit_transform(dataList)[:,0]
			
			#check correlation
			if (np.corrcoef(dataList[:,1], myPCA)[0,1] < 0):
				myPCA = myPCA * (-1)
				
				
			max = np.max(myPCA)
			myPCA = myPCA - max
			alpha = ANGLE_PC_CORRELATION_CONST *myPCA;
			
			#subtract the maximum from PCA.
			#print (p.fit_transform(dataList))
			
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

