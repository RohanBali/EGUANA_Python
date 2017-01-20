import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
from filterTypesConfig.jawFilters.joanaFilter import JoanaFilter

def testSS(ssFunction):

	ssMat = sio.loadmat('JOANNA-0010.mat')

	jawXRaw = ssMat['jawXRaw']
	jawYRaw = ssMat['jawYRaw']
	jawZRaw = ssMat['jawZRaw']
	
	jawRaw = np.concatenate((jawXRaw, jawYRaw, jawZRaw), 1)

	llXRaw = ssMat['llXRaw']
	llYRaw = ssMat['llYRaw']
	llZRaw = ssMat['llZRaw']
	
	llRaw = np.concatenate((llXRaw, llYRaw, llZRaw), 1)
	
	lhXRaw = ssMat['lhXRaw']
	lhYRaw = ssMat['lhYRaw']
	lhZRaw = ssMat['lhZRaw']
	lhRaw = np.concatenate((lhXRaw, lhYRaw, lhZRaw), 1)
	
	rhXRaw = ssMat['rhXRaw']
	rhYRaw = ssMat['rhYRaw']
	rhZRaw = ssMat['rhZRaw']
	
	rhRaw = np.concatenate((rhXRaw, rhYRaw, rhZRaw), 1)
		
	theta = ssMat['jawTheta']
	phi = ssMat['jawPhi']
	
	referenceList = np.concatenate((jawRaw,theta, phi, lhRaw, rhRaw),1)

	
	llXCorrected = ssMat['llZCorrected']

	llXCorrectedNew = (1)*(ssFunction(llRaw, referenceList))[:,2]


	plt.plot(llXCorrected)
	plt.plot(llXCorrectedNew,'r')

	plt.show()

	print(llXCorrected)
	print("Our Correction")
	print(llXCorrectedNew)
	

	if np.array_equal(llXCorrected,llXCorrectedNew):
		return True
	else:
		return False


print(testSS(JoanaFilter.filter))