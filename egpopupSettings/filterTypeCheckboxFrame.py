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
       
        for h in range(len(modifiedHeadList)):
            checkBoxVar2 = IntVar()
            headFilterCheckButton = Checkbutton(self, text=modifiedHeadList[h].name, variable=checkBoxVar2, state = DISABLED)
            self.headCheckButtonList.append(headFilterCheckButton)
            headFilterCheckButton.grid(row=1+h, column=0, sticky=W)

        for j in range(len(modifiedJawList)):
            checkBoxVar3 = IntVar()
            jawFilterCheckButton = Checkbutton(self, text=modifiedJawList[j].name, variable=checkBoxVar3, state = DISABLED)
            self.jawCheckButtonList.append(jawFilterCheckButton)
            jawFilterCheckButton.grid(row=1+j, column=1, sticky=W)

		
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
