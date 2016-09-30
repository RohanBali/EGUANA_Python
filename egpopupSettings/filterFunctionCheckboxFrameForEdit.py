from tkinter import *
from tkinter import Toplevel, RAISED, Button, TOP, X, NORMAL, DISABLED, S, N, E, W, SUNKEN, Label, OptionMenu
from tkinter.ttk import Notebook
from eguanaModel import EguanaModel
from egpopupSettings.filterFunctionCheckboxFrame import FilterFunctionCheckboxFrame


class FilterFunctionCheckboxFrameForEdit(FilterFunctionCheckboxFrame):

	def __init__(self,notebook,filterFunctionObjectList,isEnabled,enabledFilterFunctionFilenameList):

		FilterFunctionCheckboxFrame.__init__(self,notebook,filterFunctionObjectList)
		
		self.enableCheckButtonInt.set(isEnabled)
		self.enabledPressed()



		filterFunctionBoolList = []


		for ffObject in self.filterFunctionObjectList:
			filterFunctionBoolList.append(int(ffObject.getFilename() in enabledFilterFunctionFilenameList))

		for i in range(len(filterFunctionBoolList)):
			ffBool = filterFunctionBoolList[i]
			checkButtonVar = self.filterFunctionCheckButtonVarList[i]
			checkButtonVar.set(ffBool)



