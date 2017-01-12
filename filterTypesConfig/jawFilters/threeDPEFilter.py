from filterTypesConfig.eguanaFilterTypesConfig import EguanaFilterTypesConfig
import numpy as np


class ThreeDPEFilter(EguanaFilterTypesConfig):

	def __init__(self):
	
		EguanaFilterTypesConfig.__init__(self)  
		self.name = "Gold" 
		self.filterType = "Jaw"
		
	def filter (articulatorSignalList, referenceSignalList):
	
		if (articulatorSignalList.shape[1] == referenceSignalList.shape[1]):
			'''ciX,ciY,ciZ,rmX,rmY,rmZ,lmX,lmY,lmZ'''
			ciX = referenceSignalList[:,0]
			ciY = referenceSignalList[:,1]
			ciZ = referenceSignalList[:,2]
			
			rmX = referenceSignalList[:,3]
			rmY = referenceSignalList[:,4]
			rmZ = referenceSignalList[:,5]
			
			lmX = referenceSignalList[:,6]
			lmY = referenceSignalList[:,7]
			lmZ = referenceSignalList[:,8]
			
			
			rm = np.column_stack(rmX, rmY, rmZ)
			lm = np.column_stack(lmX, lmY, lmZ)
			ci = np.column_stack(ciX, ciY, ciZ)
			rh = np.column_stack(referenceSignalList[:,9], referenceSignalList[:,10], referenceSignalList[:,11])
			lh = np.column_stack(referenceSignalList[:,12], referenceSignalList[:,13], referenceSignalList[:,14])
			rlVec = rh - lh
			
			lip_Vector =(articulatorSignalList[:,0], articulatorSignalList[:, 1], articulatorSignalList[:, 2]])
			
			for i in range(len(rm.transpose[0]))
				'''head stablization'''
				'''find phi and theta'''
				
				angle_XZ_Plane = np.asin(rlVec[i][1]/np.linalg.norm(rlVec[i]))
				angle_XY_Plane = np.asin(rlVec[i][2]/np.linalg.norm(rlVec[i]))
				
				ref_Head_Xaxis = (cos(angle_XY_Plane), sin(angle_XY_Plane), 0)
				ref_Head_Yaxis = rlVec[i]/np.linalg.norm(rlVec[i])
				ref_Head_Zaxis = (0, sin(angle_XZ_Plane), cos(angle_XZ_Plane))
				
				newSys = (ref_Head_Xaxis, ref_Head_Yaxis, ref_Head_Zaxis)
				
				'''rotation'''
				rmNew = newSys*rm[:, i]
				lmNew = newSys*lm[:, i]
				ciNew = newSys*ci[:, i]
				lipNew = newSys*lip_Vector[:, i]
				'''rotated coordinates (head reference)'''
				
				
				midPoint = (rmNew + lmNew)/2
				midVec = midPoint - ciNew
				
				Rr = np.linalg.norm(rmNew - ciNew)
				Rl = np.linalg.norm(lmNew - ciNew)
				Rmid = np.linalg.norm(midVec)
				
				Ar = acos(np.dot(rmNew, midVec)/(Rmid*Rr))
				Al = acos(np.dot(lmNew, midVec)/(Rmid*Rl))
				rmNew = (-Rr*cos(Ar), -Rr*sin(Ar), 0)
				lmNew = (-Rl*cos(Al), +Rl*sin(Al), 0)
								
				newX = midVec/np.linalg.norm(midVec)
				
				newY = (lmNew-rmNew)
				newY = newY/np.linalg.norm(newY)

				newZ = np.cross(rmNew, lmNew)
				newZ = newZ/np.linalg.norm(newZ)
				
				transMatrix = (newX, newY, newZ)
				correctedList[i] = transMatrix * (lipNew - ciNew)
				
			return correctedList
		else:
			return none
			
		
			
		
	
		

