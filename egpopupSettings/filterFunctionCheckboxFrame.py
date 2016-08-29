from tkinter import *
from tkinter import Toplevel, RAISED, Button, TOP, X, NORMAL, DISABLED, S, N, E, W, SUNKEN, Label, OptionMenu
from tkinter.ttk import Notebook
from eguanaModel import EguanaModel


class FilterFunctionCheckboxFrame(Frame):
    def __init__(self,notebook,filterFunctionObjectList):
        Frame.__init__(self,notebook) 
        self.enableCheckButtonInt = IntVar()
        Checkbutton(self, text='Enabled', variable=self.enableCheckButtonInt, command=self.enabledPressed).grid(row=0, column=0, columnspan=2, sticky=N+E)

        self.filterFunctionCheckButtonList = []
       
        for h in range(len(filterFunctionObjectList)):
            checkBoxVar2 = IntVar()
            filterFunctionCheckButton = Checkbutton(self, text=filterFunctionObjectList[h].name, variable=checkBoxVar2, state = DISABLED)
            self.filterFunctionCheckButtonList.append(filterFunctionCheckButton)
            filterFunctionCheckButton.grid(row=1+h, column=0, sticky=W)

		
    def enabledPressed(self):
        
        if self.enableCheckButtonInt.get():

            for h in range(len(self.filterFunctionCheckButtonList)):
                self.filterFunctionCheckButtonList[h].config(state = NORMAL)
        else:

            for h in range(len(self.filterFunctionCheckButtonList)):
                self.filterFunctionCheckButtonList[h].config(state = DISABLED)
