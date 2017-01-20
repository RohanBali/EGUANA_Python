from filterTypesConfig.eguanaFilterTypesConfig import EguanaFilterTypesConfig
import numpy as np
import math


class JoanaFilter(EguanaFilterTypesConfig):

	def __init__(self):

		EguanaFilterTypesConfig.__init__(self)   
		self.name = "Joanna"
		self.filterType = "Jaw"
	
	def filter (articulatorSignalList, referenceSignalList):
	
		"""		
				+ve   / -ve
		x-axis: front / back
		y-axis: right / left
		z-axis: up    / down
		
		assume data of referenceSignalList is in this format (x, y, z, phi, theta, LHx, LHy, LHz, RHx, RHy, RHz)
		x,y,z are position of the jaw
		phi = azimuth (measured from +ve x-axis)
		theta = elevation (between the vector and x-y plane)
		LHx, LHy, LHz, RHx, RHy, RHz are coordinates of left and right head sensors (should be a separate input from referenceSignalList)
		"""
		
		if (articulatorSignalList.shape[0] == referenceSignalList.shape[0] ): 
			'''and articulatorSignalList.shape[1] == referenceSignalList.shape[1]'''
		
			theta = referenceSignalList[:, 3]
			phi = referenceSignalList[:, 4]

			"""x - xj & y - yj & z - zj"""
			diffX = articulatorSignalList[:, 0] - referenceSignalList[:, 0]
			diffY = articulatorSignalList[:, 1] - referenceSignalList[:, 1]
			diffZ = articulatorSignalList[:, 2] - referenceSignalList[:, 2]
			
			"""extract LH & RH position vectors"""
			'''a = ref[:,1];
			a = a.reshape(len(a),1)'''
			
			LH_Vector = referenceSignalList[:,[5,6,7]]
			'''print (LH_Vector[1])'''
			RH_Vector = referenceSignalList[:,[8,9,10]]
			print(diffX.shape)
			correctedList = np.zeros((len(diffX),3))

			for i in range (referenceSignalList.shape[0]):
			
				"""define new x,y,z axes """
				transX_axis = (-np.cos(theta[i]) * np.cos(phi[i]), -np.cos(theta[i]) * np.sin(phi[i]), -np.sin(theta[i]));   	'''converting spherical to cartisian'''				
				
				transY_axis = ( - RH_Vector[i] + LH_Vector[i])
				'''position of RH - position of LF'''
				transY_axis = transY_axis/np.linalg.norm(transY_axis)									
				'''normalized => vector t'''
				transZ_axis = np.cross(transX_axis, transY_axis) 										
				'''z-axis => x-axis cross y-axis'''
				
				np.reshape(transX_axis, (1,3))
				np.reshape(transY_axis, (1,3))
				np.reshape(transZ_axis, (1,3))
				
				transMatrix =(transX_axis, transY_axis,transZ_axis)
				transMatrix = np.reshape(transMatrix, (3,3))
				
				diffVec = np.matrix([diffX[i], diffY[i], diffZ[i]])
				
				correctedList[i] = np.transpose(transMatrix * np.transpose(diffVec));
			
			return correctedList;
		else: 
			return none;
