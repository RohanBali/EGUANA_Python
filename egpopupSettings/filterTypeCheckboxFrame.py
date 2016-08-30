from tkinter import *
from tkinter import Toplevel, RAISED, Button, TOP, X, NORMAL, DISABLED, S, N, E, W, SUNKEN, Label, OptionMenu
from tkinter.ttk import Notebook
from eguanaModel import EguanaModel


class FilterTypeCheckboxFrame(Frame):
    def __init__(self,notebook,modifiedHeadList,modifiedJawList):
        Frame.__init__(self,notebook) 
        self.enableCheckButtonInt = IntVar()
        Checkbutton(self, text='Enabled', variable=self.enableCheckButtonInt, command=self.enabledPressed).grid(row=0, column=0, columnspan=2, sticky=N+E)

        self.headCheckButtonList = []
        self.jawCheckButtonList = []

        self.headCheckButtonVarList = []
        self.jawCheckButtonVarList = []

        self.headObjectList = modifiedHeadList
        self.jawObjectList = modifiedJawList

       
        for h in range(len(modifiedHeadList)):
            checkBoxVar2 = IntVar()
            headFilterCheckButton = Checkbutton(self, text=modifiedHeadList[h].name, variable=checkBoxVar2, state = DISABLED)
            self.headCheckButtonList.append(headFilterCheckButton)
            headFilterCheckButton.grid(row=1+h, column=0, sticky=W)
            self.headCheckButtonVarList.append(checkBoxVar2)

        for j in range(len(modifiedJawList)):
            checkBoxVar3 = IntVar()
            jawFilterCheckButton = Checkbutton(self, text=modifiedJawList[j].name, variable=checkBoxVar3, state = DISABLED)
            self.jawCheckButtonList.append(jawFilterCheckButton)
            jawFilterCheckButton.grid(row=1+j, column=1, sticky=W)
            self.jawCheckButtonVarList.append(checkBoxVar3)
		
    def enabledPressed(self):
        
        if self.enableCheckButtonInt.get():

            for h in range(len(self.headCheckButtonList)):
                self.headCheckButtonList[h].config(state = NORMAL)

            for j in range(len(self.jawCheckButtonList)):
                self.jawCheckButtonList[j].config(state = NORMAL)

        else:

            for h in range(len(self.headCheckButtonList)):
                self.headCheckButtonList[h].config(state = DISABLED)

            for j in range(len(self.jawCheckButtonList)):
                self.jawCheckButtonList[j].config(state = DISABLED)            



    def isEnabled(self):
        return self.enableCheckButtonInt.get()


    def getEnabledHeadFilterTypeNames(self):    
        
        enabledHeadFilterTypeNames = []

        for i in range(len(self.headCheckButtonVarList)):
            if self.headCheckButtonVarList[i].get():
                enabledHeadFilterTypeNames.append(self.headObjectList[i].getFilename())

        return enabledHeadFilterTypeNames





    def getEnabledJawFilterTypeNames(self):    

        enabledJawFilterTypeNames = []

        for i in range(len(self.jawCheckButtonVarList)):
            if self.jawCheckButtonVarList[i].get():
                enabledJawFilterTypeNames.append(self.jawObjectList[i].getFilename())


        return enabledJawFilterTypeNames
