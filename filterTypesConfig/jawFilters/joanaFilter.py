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
		
			theta = referenceSignalList.transpose[4];
			phi = referenceSignalList.transpose[3];
			
			"""x - xj & y - yj & z - zj"""
			diffX = articulatorSignalList.transpose[0] - referenceSignalList.transpose[0];
			diffY = articulatorSignalList.transpose[1] - referenceSignalList.transpose[1];
			diffZ = articulatorSignalList.transpose[2] - referenceSignalList.transpose[2];
			
			"""extract LH & RH position vectors"""
			LH_Vector = np.column_stack (referenceSignalList[:,5], referenceSignalList[:,6], referenceSignalList[:,7])
			RH_Vector = np.column_stack (referenceSignalList[:,8], referenceSignalList[:,9], referenceSignalList[:,10])

			for i in range (len(referenceSignalList[0])):
			
				"""define new x,y,z axes """
				transX_axis = (cos(theta[0][i])*cos(phi[0][i]), cos(theta[0][i])*sin(phi[0][i]), sin(theta[0][i]));   	'''converting spherical to cartisian'''				
				transY_axis = (RH_Vector[i] - LH_Vector[i]); 										   	'''position of RH - position of LF'''
				transY_axis = transY_axis/np.linalg.norm(transY_axis);									'''normalized => vector t'''
				transZ_axis = np.cross(transX_axis, transY_axis); 										'''z-axis => x-axis cross y-axis'''
				
				transMatrix = (transX_axis, transY_axis, transZ_axis);
				diffVec = (diffX[0][i], diffY[0][i], diffZ[0][i]);
				
				correctedList[i] = transMatrix * diffVec.transpose();
			
			return correctedList;
		else: 
			return none;
