from filterTypesConfig.eguanaFilterTypesConfig import EguanaFilterTypesConfig
import numpy as np

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
		
		if (articulatorSignalList.shape[0] == referenceSignalList.shape[0] and articulatorSignalList.shape[1] == referenceSignalList.shape[1]):
		
			theta = referenceSignalList.T[4];
			phi = referenceSignalList.T[3];
			
			"""x - xj & y - yj & z - zj"""
			diffX = articulatorSignalList.T[0] - referenceSignalList.T[0];
			diffY = articulatorSignalList.T[1] - referenceSignalList.T[1];
			diffZ = articulatorSignalList.T[2] - referenceSignalList.T[2];
			
			"""extract LH & RH position vectors"""
			LH_Vector = referenceSignalList[[:,5], [:,6], [:,7]];
			RH_Vector = referenceSignalList[[:,8], [:,9], [:,10]];

			for i in range (len(referenceSignalList[0])):
			
				"""define new x,y,z axes """
				transX_axis = (cos(theta[i])*cos(phi[i]), cos(theta[i])*sin(phi[i]), sin(theta[i]));   	'''converting spherical to cartisian'''				
				transY_axis = (RH_Vector[i] - LH_Vector[i]); 										   	'''position of RH - position of LF'''
				transY_axis = transY_axis/np.linalg.norm(transY_axis);									'''normalized => vector t'''
				transZ_axis = np.cross(transX_axis, transY_axis); 										'''z-axis => x-axis cross y-axis'''
				
				transMatrix = (transX_axis, transY_axis, transZ_axis);
				diffVec = (diffX[i], diffY[i], diffZ[i]);
				
				correctedList[i] = transMatrix * diffVec;
			
			return correctedList;
		else: 
			return none;
