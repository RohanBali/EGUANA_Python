from tkinter import *
from tkinter import Toplevel, RAISED, Button, TOP, X, NORMAL, DISABLED, S, N, E, W, SUNKEN, Label, OptionMenu
from tkinter.ttk import Notebook
from eguanaModel import EguanaModel
from egpopupSettings.filterTypeCheckboxFrame import FilterTypeCheckboxFrame


class FilterTypeCheckboxFrameForEdit(FilterTypeCheckboxFrame):

	def __init__(self,notebook, headObjectList,jawObjectList,isEnabled,enabledJawFilenameList,enabledHeadFilenameList):

		FilterTypeCheckboxFrame.__init__(self,notebook,headObjectList,jawObjectList)
		self.enableCheckButtonInt.set(isEnabled)
		self.enabledPressed()


		jawBoolList = []
		headBoolList = []

		for headObject in self.headObjectList:
			headBoolList.append(int(headObject.getFilename() in  enabledHeadFilenameList))


		for jawObject in self.jawObjectList:
			jawBoolList.append(int(jawObject.getFilename() in  enabledJawFilenameList))



		for i in range(len(jawBoolList)):
			jawBool = jawBoolList[i]
			checkButtonVar = self.jawCheckButtonVarList[i]
			checkButtonVar.set(jawBool)



		for i in range(len(headBoolList)):
			headBool = headBoolList[i]
			checkButtonVar = self.headCheckButtonVarList[i]
			checkButtonVar.set(headBool)

