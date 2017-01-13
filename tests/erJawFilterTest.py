import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
from filterTypesConfig.jawFilters.erFilter import ErFilter

def testSS(ssFunction):

	ssMat = sio.loadmat('ER-0010.mat')

	jawXRaw = ssMat['jawXRaw']
	jawYRaw = ssMat['jawYRaw']
	jawZRaw = ssMat['jawZRaw']
	
	jawRaw = np.concatenate((jawXRaw, jawYRaw, jawZRaw), 1)

	llXRaw = ssMat['llXRaw']
	llYRaw = ssMat['llYRaw']
	llZRaw = ssMat['llZRaw']
	
	llRaw = np.concatenate((llXRaw, llYRaw, llZRaw), 1)

	
	
	llYCorrected = ssMat['llXCorrected']

	llXCorrectedNew = (ssFunction(llRaw, jawRaw))[:,0]


	plt.plot(llYCorrected)
	plt.plot(llXCorrectedNew,'r')

	plt.show()

	print(llYCorrected)
	print("Our Correction")
	print(llXCorrectedNew)

	if np.array_equal(llYCorrected,llXCorrectedNew):
		return True
	else:
		return False

def ss(jawP,sensorP):
	return sensorP-jawP


print(testSS(ErFilter.filter))