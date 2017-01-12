import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
from filterTypesConfig.jawFilters.ssFilter import SsFilter

def testSS(ssFunction):

	ssMat = sio.loadmat('SS-0010.mat')

	jawXRaw = ssMat['jawXRaw']

	llXRaw = ssMat['llXRaw']

	llXCorrected = ssMat['llXCorrected']


	llXCorrectedNew = ssFunction(jawXRaw,llXRaw)


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

def ss(jawP,sensorP):
	return sensorP-jawP


print(testSS(SsFilter.filter))