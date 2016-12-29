import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt

def testSS(ssFunction):

	ssMat = sio.loadmat('../SS-0010.mat')

	jawXRaw = ssMat['jawXRaw']
	jawYRaw = ssMat['jawYRaw']
	jawZRaw = ssMat['jawZRaw']

	llXRaw = ssMat['llXRaw']
	llYRaw = ssMat['llYRaw']
	llZRaw = ssMat['llZRaw']

	llXCorrected = ssMat['llXCorrected']
	llYCorrected = ssMat['llYCorrected']
	llZCorrected = ssMat['llZCorrected']


	llXCorrectedNew = ssFunction(jawXRaw,llXRaw)
	llYCorrectedNew = ssFunction(jawYRaw,llYRaw)
	llZCorrectedNew = ssFunction(jawZRaw,llZRaw)

	print(llXCorrected)
	print("Our Correction")
	print(llXCorrectedNew)

	if np.array_equal(llXCorrected,llXCorrectedNew) and np.array_equal(llYCorrected,llYCorrectedNew) and np.array_equal(llZCorrected,llZCorrectedNew):
		return True
	else:
		return False

def ss(jawP,sensorP):
	return sensorP-jawP


print(testSS(ss))